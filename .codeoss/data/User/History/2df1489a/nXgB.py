def google_search_query(player_name: str):
    print("google_search_query", player_name)
    prompt = f"Generate a scouting report for the minor league player {player_name} for the 2024 and 2023 season."

    try:
        # Initialize the Google Search tool
        google_search_tool = Tool(google_search=GoogleSearch())
        
        # Generate content stream
        response_stream = client.models.generate_content_stream(
            model=GOOGLE_MODEL_ID,
            contents=[prompt],
            config=GenerateContentConfig(
                system_instruction=sys_instruction,
                tools=[google_search_tool],
                temperature=0
            ),
        )
        
        # Initialize a buffer to capture the response
        report = io.StringIO()
        
        # Iterate over the response stream
        for chunk in response_stream:
            print(chunk)  # Debug: Print each chunk
            candidate = chunk.candidates[0]
            for part in candidate.content.parts:
                if part.text:
                    report.write(part.text)
                else:
                    print(json.dumps(part.model_dump(exclude_none=True), indent=2))
        
        # Get the final scouting report from the buffer
        scouting_report = report.getvalue()
        
        return scouting_report
    except Exception as e:
        print(f"An error occurred: {e}")
        return None