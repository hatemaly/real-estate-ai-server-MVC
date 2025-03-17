# @title implmentation of vector store weaviate.
import os
from typing import List
import weaviate.classes as wvc
from httpx import Auth
from langchain.vectorstores import weaviate
from langsmith.schemas import DataType
from weaviate.collections.classes.config import Configure

from app.models.property_models.property import Property


class VectorDBWeaviate:

    def connect(self):
        cluster_url="https://khyfid1rtefnmjyeahzrg.c0.europe-west3.gcp.weaviate.cloud"

        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=cluster_url,
            auth_credentials=Auth.api_key(os.getenv("ADMIN_KEY")),
        )

    def disconnect(self):
        self.client = None

    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collections.exists(collection_name)


    def list_all_collections(self) -> List:
        return self.client.collections.list_all(simple=True)

    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.collections.get(collection_name).config.get()

    def delete_collection(self, collection_name: List[str]) -> None:
        self.client.collections.delete(collection_name)


    def create_collection(self, collection_name: str,
                                embedding_size: int = 512,
                                do_reset: bool = False) -> bool:

        is_exist = self.is_collection_existed(collection_name)

        if is_exist and do_reset:
            self.delete_collection(collection_name)
        elif is_exist:
            return False

        self.client.collections.create(
            collection_name,
            vectorizer_config=Configure.Vectorizer.text2vec_openai(
                model="text-embedding-3-small",
                dimensions=embedding_size
            ),
            description="A collection of news articles",
            properties=[  # properties configuration is optional
                Property(name="property_id", data_type=DataType.UUID,description="The property id (uuid)"),
                Property(name="content", data_type=DataType.TEXT,description="The main content of the property"),
            ]
        )
        return True


    def insert_one(self, collection_name: str, text: str, vector: list, metadata: dict = None):

        collection = self.client.collections.get(collection_name)
        data = {
            "property_id": metadata.get("property_id"),
            "content": text
        }
        uuid = collection.data.insert(
            properties=data,
            vector=vector
        )

        return uuid

    def insert_many(self, collection_name: str, texts: list,
                          vectors: list, metadata: list = None,
                          record_ids: list = None, batch_size: int = 50):
        pass


    def search_by_vector(self, collection_name: str, vector: list, limit: int):
        collection = self.client.collections.get(collection_name)

        # Perform similarity search
        response = collection.query.near_vector(
            near_vector=vector,
            limit=1,
            return_metadata=wvc.query.MetadataQuery(
                distance=True,  # Explicitly request distance scores
                score=True,  # Explicitly request similarity scores
                certainty=True,  # Explicitly request certainty scores
                explain_score=True,
                is_consistent=True,

            )
        )

        results = []
        for obj in response.objects:
            results.append({
                "property_id": obj.properties["property_id"],
                "content": obj.properties["content"],
                "distance": obj.metadata.distance,  # The similarity score
                "score": obj.metadata.score,  # The similarity score
                "certainty": obj.metadata.certainty,
            })

        return results

    def retrieve_location_ids(self, location_names: List[str]) -> List[str]:
        """
        Retrieve IDs for a list of location names from the Locations collection
        using near_vector semantic search

        Args:
            location_names: List of location names to retrieve IDs for

        Returns:
            List of location IDs corresponding to the provided names
        """
        collection = self.client.collections.get("Locations")
        location_ids = []

        for location_name in location_names:
            # Get vector embedding for the location name
            vector = self._get_embedding(location_name)

            # Perform near_vector search
            response = collection.query.near_vector(
                near_vector=vector,
                limit=1,
                return_properties=["property_id", "content"],
                return_metadata=wvc.query.MetadataQuery(
                    certainty=True
                )
            )

            if response.objects and len(response.objects) > 0:
                # You might want to add a certainty threshold here
                if response.objects[0].metadata.certainty > 0.7:  # Adjust threshold as needed
                    location_ids.append(response.objects[0].properties["property_id"])
                else:
                    location_ids.append(None)  # Below certainty threshold
            else:
                location_ids.append(None)

        return location_ids

    def retrieve_developer_ids(self, developer_names: List[str]) -> List[str]:
        """
        Retrieve IDs for a list of developer names from the Developers collection
        using near_vector semantic search

        Args:
            developer_names: List of developer names to retrieve IDs for

        Returns:
            List of developer IDs corresponding to the provided names
        """
        collection = self.client.collections.get("Developers")
        developer_ids = []

        for developer_name in developer_names:
            # Get vector embedding for the developer name
            vector = self._get_embedding(developer_name)

            # Perform near_vector search
            response = collection.query.near_vector(
                near_vector=vector,
                limit=1,
                return_properties=["property_id", "content"],
                return_metadata=wvc.query.MetadataQuery(
                    certainty=True
                )
            )

            if response.objects and len(response.objects) > 0:
                # You might want to add a certainty threshold here
                if response.objects[0].metadata.certainty > 0.7:  # Adjust threshold as needed
                    developer_ids.append(response.objects[0].properties["property_id"])
                else:
                    developer_ids.append(None)  # Below certainty threshold
            else:
                developer_ids.append(None)

        return developer_ids

    def retrieve_project_ids(self, project_names: List[str]) -> List[str]:
        """
        Retrieve IDs for a list of project names from the Projects collection
        using near_vector semantic search

        Args:
            project_names: List of project names to retrieve IDs for

        Returns:
            List of project IDs corresponding to the provided names
        """
        collection = self.client.collections.get("Projects")
        project_ids = []

        for project_name in project_names:
            # Get vector embedding for the project name
            vector = self._get_embedding(project_name)

            # Perform near_vector search
            response = collection.query.near_vector(
                near_vector=vector,
                limit=1,
                return_properties=["property_id", "content"],
                return_metadata=wvc.query.MetadataQuery(
                    certainty=True
                )
            )

            if response.objects and len(response.objects) > 0:
                # You might want to add a certainty threshold here
                if response.objects[0].metadata.certainty > 0.7:  # Adjust threshold as needed
                    project_ids.append(response.objects[0].properties["property_id"])
                else:
                    project_ids.append(None)  # Below certainty threshold
            else:
                project_ids.append(None)

        return project_ids

    def _get_embedding(self, text: str) -> list:
        """
        Helper method to get embedding for a text using the OpenAI API
        Replace this with your actual embedding generation logic
        """
        # This is a placeholder - you should implement your actual embedding generation
        # Example implementation using OpenAI:
        import openai

        response = openai.Embedding.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding