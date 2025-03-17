# @title testing
import json

from app.agents.MessageFormatExtractionAgent import MessageFormatExtractionAgent

test_messages = [
    # Test 1: Basic property with most fields
    """I'm looking for a 3-bedroom, 2-bathroom apartment in Downtown Cairo, preferably developed by Emaar or SODIC.
    My budget is between 2,000,000 to 3,500,000 EGP. The apartment should be around 150 square meters, fully finished,
    and have at least 1 parking space. I prefer residential properties with amenities like a swimming pool and a garden.""",

    # # Test 2: Testing commercial properties and different currency
    # """Our company is interested in leasing an office space in Maadi or New Cairo. We're looking at Class A commercial
    # buildings with 400-600 square meters. Budget is flexible but preferably under $15,000 USD per month. The office should
    # be semi-finished so we can customize it to our needs. We're interested in MNHD or Palm Hills developments with
    # delivery expected by June 2025.""",
    #
    # # Test 3: Villa with specific amenities
    # """I want to purchase a luxury villa in Uptown Cairo or La Vista developments. The property should be at least
    # 350 square meters with 5 bedrooms, 4 bathrooms, and 2 parking spaces. Must have a swimming pool and garden.
    # My budget is 12-15 million EGP for a fully finished property. Ideally in a gated community with 24/7 security.""",
    #
    # # Test 4: Industrial property
    # """Looking for an industrial facility in 6th of October Industrial Zone or 10th of Ramadan City. Need at least
    # 2000 square meters of unfinished space that can be converted to a manufacturing plant. Budget is approximately
    # 4-7 million EUR depending on location and specifications. Prefer properties developed by Industrial Development Group.""",
    #
    # # Test 5: Multiple property types in one message
    # """I'm a real estate investor looking at several options: either apartments in New Administrative Capital (NAC)
    # priced between 1.5-2.5 million EGP, or office spaces in Smart Village for about 3-4 million EGP. For residential
    # properties, I prefer 2 bedrooms and at least 100 square meters. For commercial, I need at least 150 square meters.
    # Interested in projects by SODIC, Talaat Moustafa Group, or Mountain View.""",
    #
    # # Test 6: Minimal information
    # """Are there any properties available in Sheikh Zayed City?""",
    #
    # # Test 7: Testing delivery date extraction
    # """I'm interested in pre-construction projects in El Gouna or Soma Bay that will be delivered by Q4 2026.
    # Looking for a residential villa or apartment, preferably semi-finished, with sea view. My budget is flexible
    # but ideally under 8 million EGP.""",
    #
    # # Test 8: Testing with British pounds and specific project
    # """I'm a British expat looking to invest in Cairo Festival City. I'm specifically interested in the Oriana
    # Villas project or something similar. My budget is around £300,000 to £450,000. I want a property with
    # at least 4 bedrooms and must have a private garden and pool. Preferably fully finished and ready to move in.""",
    #
    # # Test 9: Testing with multiple numeric values that could be confused
    # """I'm looking for a 2-floor apartment in Heliopolis with 3 bedrooms and 2 bathrooms. The building should not be
    # more than 5 years old. Looking to pay around 8000 EGP per month for rent. The apartment should be at least on the
    # 3rd floor of the building and have a balcony facing the street.""",
    #
    # # Test 10: Testing edge case with no clear property type but other information
    # """I'm relocating to Alexandria and need a place with a sea view. My budget is up to 1.2 million EGP.
    # I need at least 120 square meters of living space. The property should be in a safe neighborhood with good
    # access to schools and shopping centers.""",
    #
    # """I'm thinking about maybe investing in some property in Egypt. What areas are good these days?""",
    #

]

# Example of running the tests
agent = MessageFormatExtractionAgent()

for i, message in enumerate(test_messages, 1):
    print(f"\n--- Test {i} ---")
    print(f"Message: {message[:100]}...")

    result = agent.execute(message)

    print("Extracted Information:")
    print(json.dumps(result, indent=4))

    # Check for any error
    if "error" in result:
        print(f"ERROR: {result['error']}")