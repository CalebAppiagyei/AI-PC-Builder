from openai import OpenAI

def get_recommendations(client: OpenAI, prompt: str) -> str:
    print("\nConsulting GPT-4o for your personalized build recommendations...\n")
    print("=" * 60)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior PC hardware expert. "
                    "You have deep knowledge of CPU socket compatibility, chipset features, "
                    "RAM DDR generations, PSU sizing, case form factors, GPU power requirements, "
                    "NVMe generations, and current market pricing as of early 2025. "
                    "You independently verify compatibility rather than just repeating automated checks. "
                    "You prioritize recommending the best parts for the user's use case and budget "
                    "over sticking to the user's stated preferences — if a better option exists, "
                    "you recommend it and explain why. "
                    "You are direct and specific: you name exact incompatibilities, explain the "
                    "physical or electrical reason they fail, and always suggest a concrete fix."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=2500,
    )
    return response.choices[0].message.content
