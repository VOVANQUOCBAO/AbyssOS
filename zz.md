Purpose
This guide is designed for participants of the Video Generation Track, co-hosted by PixVerse.

In this track, you will use TRAE as your AI agent and IDE to build a web page, website, or app that integrates an AI-generated video of at least 30 seconds, produced using PixVerse.

The project should serve one of the following domains:

- Marketing / E-commerce
- Gaming
- Film & Entertainment
  
The video should be a meaningful content component inside a functional product experience, such as a product demo, campaign video, game trailer, character showcase, movie clip, scene breakdown, or interactive pitch asset.

This is not a video generation tool track. Your app or web experience must provide practical functionality beyond playback, such as product interaction, purchasing flow, comments, voting, personalization, game lore exploration, scene navigation, or community engagement.

You will be evaluated on PixVerse video quality & creative direction (40%), app/web completeness, UX & integration (30%), and TRAE workflow depth & efficiency gain (30%). See the full criteria in the track rules.


Step 1: Define the Product Experience
Start with user experience, not the video alone.

Ask:
- Who is the target user?
- What is the page or app supposed to help them do?
- How does the PixVerse video improve the experience?
- What functionality exists beyond playback?
  
Examples:
- Marketing / E-commerce: product discovery, campaign landing page, product demo, purchasing flow
- Gaming: game world page, character showcase, trailer experience, lore exploration
- Film & Entertainment: movie pitch page, scene breakdown, interactive teaser, fan engagement page
  
Step 2: Plan the Video as Short Shots
Do not try to generate the full video in one step. Break the concept into short clips.

Recommended structure:
- 4 to 8 shots
- 5 to 8 seconds per shot
- At least 30 seconds in final assembled video
- 720p for drafts, higher quality for final output if credits allow
- 9:16 for vertical social-style videos, 16:9 for cinematic or presentation-style videos
  
Suggested prompt:
“Please break my video idea into a series of shots. For each shot, include:
1. Scene description
2. Camera movement
3. Subject action
4. PixVerse prompt
5. Suggested duration
6. Aspect ratio
7. Model and quality recommendation”
  
Step 3: Generate with PixVerse
Use PixVerse through the workflow your team is most comfortable with:

- PixVerse web app
- PixVerse CLI
- PixVerse Skills
- TRAE-assisted workflow using prompts, scripts, or automation
  
If you choose the CLI and Skills workflow, you can ask TRAE:
“Help me install and use PixVerse CLI and PixVerse Skills from:
https://github.com/PixVerseAI/skills”

Then ask TRAE to load the Skills entry file:
“Please load skills/SKILL.md as the entry point, then guide me through the PixVerse video generation workflow.”

Basic CLI commands, if your team uses CLI:
npm install -g pixverse
pixverse auth login

Security reminder: Do not place account credentials, tokens, or authentication data in your project files, Git repository, screenshots, or final submission.

Step 4: Use PixVerse V6 When Appropriate
PixVerse V6 is the default PixVerse video model and is suitable for high-quality general video generation.

It supports video generation, transitions, and extend workflows, with multiple resolutions, durations up to 15 seconds per generation, and common aspect ratios.

Use V6 for:
- Marketing videos
- Product demos
- Game trailers
- Character showcases
- Cinematic or commercial-style clips
- Multi-shot visual storytelling
  
Example TRAE prompt:
“Use PixVerse V6 to generate a 6-second 16:9 shot for a product launch video. Include subject action, camera movement, lighting, visual style, and scene purpose.”

Step 5: Review, Improve, and Assemble
For each shot:
1. Ask TRAE to write or improve the PixVerse prompt.
2. Generate a short clip with PixVerse.
3. Review visual quality, pacing, relevance, and consistency.
4. Improve weak shots only.
5. Assemble the final video so the total duration is at least 30 seconds.
6. Embed the video inside your app or web experience.
  
Strong PixVerse prompts usually include:
- Subject and setting
- Action and camera movement
- Lighting and visual style
- Emotion or atmosphere
- Duration and aspect ratio
- Product, character, or world consistency
  
Step 6: Use TRAE Deeply
TRAE is part of the judging criteria, so show how it helped your team work faster or better.

Use TRAE for:
- Ideation and concept refinement
- Script and storyboard generation
- PixVerse prompt writing and iteration
- Web/app coding
- Debugging
- Automation
- Workflow orchestration, including SOLO MTC where applicable
  
SOLO MTC refers to TRAE SOLO’s multi-task collaboration workflow for coordinating multiple agentic tasks, such as planning, coding, debugging, prompt generation, and iteration within one project workflow.

In your final write-up, explain how TRAE improved speed, quality, automation, or collaboration.

Step 7: Build the App/Web Experience
Your video should be integrated into a real product experience.

Good examples:
- A product page where the video explains the product and supports purchase intent
- A campaign page where the video drives interaction or conversion
- A game page where the video introduces a character, world, or storyline
- A film page where the video supports a scene breakdown, pitch, or fan experience
  
Avoid:
- A standalone video player
- A pure video generation interface
- A page where the video is decorative but not meaningful
- A demo with no functional user flow
  
Final Submission Checklist
Submit:
- Source code
- Working demo link
- Final PixVerse-generated video, at least 30 seconds 
- Brief write-up covering creative concept, target domain and user experience, PixVerse usage, TRAE usage, key prompts or workflow highlights, and any efficiency gains, faster iteration, or meaningful automation
  
Fastest On-site Workflow
1. Choose one domain: Marketing/E-commerce, Gaming, or Film & Entertainment.
2. Define the user experience and functionality beyond playback.
3. Ask TRAE to split the video idea into shots.
4. Generate short clips with PixVerse.
5. Review and improve the strongest shots.
6. Assemble a final video of at least 30 seconds.
7. Use TRAE to build the web/app experience and embed the video.
8. Prepare the demo link, source code, final video, and short write-up.
  
Troubleshooting
Issue
What to Check
No credits or generation blocked
Confirm PixVerse account status, plan, or available credits.
Output is not as expected
Improve prompt clarity: subject, action, camera movement, style, and scene purpose.
Video feels disconnected from app
Rework the user journey, so the video supports product, story, or interaction.
App is too simple
Add meaningful functionality beyond playback: interaction, comments, purchasing, voting, navigation, or personalization.
TRAE usage is unclear
Document where TRAE helped with ideation, prompts, coding, debugging, automation, or SOLO MTC-style workflow orchestration.
Need 30+ seconds
Generate multiple short clips, then assemble them into one final video.


