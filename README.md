# GPT-4V Powered Smartphone Automation
Leveraging the OpenAI GPT-4V model, you can automate your everyday tasks on an Android device. The agent looks and operates your smartphone just like a human.

> ⚠️ This is an experimental project. The correctness of the agent's actions is not guaranteed. Use it at your own risk.

## Demos
Here are some demo videos. The live screen is shown on the left, and what GPT-4V sees is shown on the right. Videos are speeded up for better viewability.
### Simple task
Task: Call 123.

The agent is able to locate the "Phone" app and dial to number 123.

https://github.com/LLM-smartphone/llm-smartphone-project/assets/22321356/e066516b-ca62-4b88-b8a4-605d8620838b

### Complicated task
Task: Open TikTok and like videos of ladies but not of males.

The agent automatically scrolls to the next video and only clicks the like button when the actor is female.


https://github.com/LLM-smartphone/llm-smartphone-project/assets/22321356/029fd404-44b0-4900-a1ce-875704356533


### Error handling
Task: Turn on dark mode.

While finding the dark mode button, the agent falsely navigates to the "Sounds and Vibration" page. Then, it realizes the mistake and corrects itself by navigating back.

https://github.com/LLM-smartphone/llm-smartphone-project/assets/22321356/e0b6ca91-f1e7-48f9-ada7-a72c9a503860

## Quick start guide
1. Register an OpenAI API account, add the OpenAI token as an env variable `OPENAI_API_KEY`
2. Make a payment to OpenAI (~$10 should be good). This is required to get GPT4-V access. You may need to wait for a few hours before getting the access.
3. Install Anaconda (https://www.anaconda.com/)
4. Create our virtual environment `conda env create -f environment.yml` and activate it `conda activate android`
5. Download AndroidStudio, and launch the default Google Pixel emulator (either from command line or GUI).
6. Start ADB: `adb -e shell`
7. Execute the `agent.py` file.


