Getting Started
Introduction
A new way to use computers

​
thumbnail
Open Interpreter lets language models run code.

You can chat with Open Interpreter through a ChatGPT-like interface in your terminal by running interpreter after installing.

This provides a natural-language interface to your computer’s general-purpose capabilities:

Create and edit photos, videos, PDFs, etc.
Control a Chrome browser to perform research
Plot, clean, and analyze large datasets
…etc.

You can also build Open Interpreter into your applications with our Python package.
​
Quick start
If you already use Python, you can install Open Interpreter via pip:

Install


Copy

Ask AI
pip install open-interpreter
Use


Copy

Ask AI
interpreter

Installation from pip
If you are familiar with Python, we recommend installing Open Interpreter via pip


Copy

Ask AI
pip install open-interpreter
You’ll need Python 3.10 or 3.11. Run python --version to check yours.

It is recommended to install Open Interpreter in a virtual environment.

​
Install optional dependencies from pip
Open Interpreter has optional dependencies for different capabilities

Local Mode dependencies


Copy

Ask AI
pip install open-interpreter[local]
OS Mode dependencies


Copy

Ask AI
pip install open-interpreter[os]
Safe Mode dependencies


Copy

Ask AI
pip install open-interpreter[safe]
Server dependencies


Copy

Ask AI
pip install open-interpreter[server]
​
Experimental one-line installers
To try our experimental installers, open your Terminal with admin privileges (click here to learn how), then paste the following commands:


Mac

Windows

Linux

Copy

Ask AI
curl -sL https://raw.githubusercontent.com/KillianLucas/open-interpreter/main/installers/oi-mac-installer.sh | bash
These installers will attempt to download Python, set up an environment, and install Open Interpreter for you.

​
No Installation
If configuring your computer environment is challenging, you can press the , key on the GitHub page to create a codespace. After a moment, you’ll receive a cloud virtual machine environment pre-installed with open-interpreter. You can then start interacting with it directly and freely confirm its execution of system commands without worrying about damaging the system.

Settings
All Settings
Language Model Settings
Set your model, api_key, temperature, etc.

Interpreter Settings
Change your system_message, set your interpreter to run offline, etc.

Code Execution Settings
Modify the interpreter.computer, which handles code execution.

​
Language Model
​
Model Selection
Specifies which language model to use. Check out the models section for a list of available models. Open Interpreter uses LiteLLM under the hood to support over 100+ models.


Terminal

Python

Profile

Copy

Ask AI
interpreter --model "gpt-3.5-turbo"
​
Temperature
Sets the randomness level of the model’s output. The default temperature is 0, you can set it to any value between 0 and 1. The higher the temperature, the more random and creative the output will be.


Terminal

Python

Profile

Copy

Ask AI
interpreter --temperature 0.7
​
Context Window
Manually set the context window size in tokens for the model. For local models, using a smaller context window will use less RAM, which is more suitable for most devices.


Terminal

Python

Profile

Copy

Ask AI
interpreter --context_window 16000
​
Max Tokens
Sets the maximum number of tokens that the model can generate in a single response.


Terminal

Python

Profile

Copy

Ask AI
interpreter --max_tokens 100
​
Max Output
Set the maximum number of characters for code outputs.


Terminal

Python

Profile

Copy

Ask AI
interpreter --max_output 1000
​
API Base
If you are using a custom API, specify its base URL with this argument.


Terminal

Python

Profile

Copy

Ask AI
interpreter --api_base "https://api.example.com"
​
API Key
Set your API key for authentication when making API calls. For OpenAI models, you can get your API key here.


Terminal

Python

Profile

Copy

Ask AI
interpreter --api_key "your_api_key_here"
​
API Version
Optionally set the API version to use with your selected model. (This will override environment variables)


Terminal

Python

Profile

Copy

Ask AI
interpreter --api_version 2.0.2
​
LLM Supports Functions
Inform Open Interpreter that the language model you’re using supports function calling.


Terminal

Python

Profile

Copy

Ask AI
interpreter --llm_supports_functions
​
LLM Does Not Support Functions
Inform Open Interpreter that the language model you’re using does not support function calling.


Terminal

Python

Profile

Copy

Ask AI
interpreter --no-llm_supports_functions
​
Execution Instructions
If llm.supports_functions is False, this value will be added to the system message. This parameter tells language models how to execute code. This can be set to an empty string or to False if you don’t want to tell the LLM how to do this.


Python

Profile

Copy

Ask AI
interpreter.llm.execution_instructions = "To execute code on the user's machine, write a markdown code block. Specify the language after the ```. You will receive the output. Use any programming language."
​
LLM Supports Vision
Inform Open Interpreter that the language model you’re using supports vision. Defaults to False.


Terminal

Python

Profile

Copy

Ask AI
interpreter --llm_supports_vision
​
Interpreter
​
Vision Mode
Enables vision mode, which adds some special instructions to the prompt and switches to gpt-4o.


Terminal

Python

Profile

Copy

Ask AI
interpreter --vision
​
OS Mode
Enables OS mode for multimodal models. Currently not available in Python. Check out more information on OS mode here.


Terminal

Profile

Copy

Ask AI
interpreter --os
​
Version
Get the current installed version number of Open Interpreter.


Terminal

Copy

Ask AI
interpreter --version
​
Open Local Models Directory
Opens the models directory. All downloaded Llamafiles are saved here.


Terminal

Copy

Ask AI
interpreter --local_models
​
Open Profiles Directory
Opens the profiles directory. New yaml profile files can be added to this directory.


Terminal

Copy

Ask AI
interpreter --profiles
​
Select Profile
Select a profile to use. If no profile is specified, the default profile will be used.


Terminal

Copy

Ask AI
interpreter --profile local.yaml
​
Help
Display all available terminal arguments.


Terminal

Copy

Ask AI
interpreter --help
​
Loop (Force Task Completion)
Runs Open Interpreter in a loop, requiring it to admit to completing or failing every task.


Terminal

Python

Profile

Copy

Ask AI
interpreter --loop
​
Verbose
Run the interpreter in verbose mode. Debug information will be printed at each step to help diagnose issues.


Terminal

Python

Profile

Copy

Ask AI
interpreter --verbose
​
Safe Mode
Enable or disable experimental safety mechanisms like code scanning. Valid options are off, ask, and auto.


Terminal

Python

Profile

Copy

Ask AI
interpreter --safe_mode ask
​
Auto Run
Automatically run the interpreter without requiring user confirmation.


Terminal

Python

Profile

Copy

Ask AI
interpreter --auto_run
​
Max Budget
Sets the maximum budget limit for the session in USD.


Terminal

Python

Profile

Copy

Ask AI
interpreter --max_budget 0.01
​
Local Mode
Run the model locally. Check the models page for more information.


Terminal

Python

Profile

Copy

Ask AI
interpreter --local
​
Fast Mode
Sets the model to gpt-3.5-turbo and encourages it to only write code without confirmation.


Terminal

Profile

Copy

Ask AI
interpreter --fast
​
Custom Instructions
Appends custom instructions to the system message. This is useful for adding information about your system, preferred languages, etc.


Terminal

Python

Profile

Copy

Ask AI
interpreter --custom_instructions "This is a custom instruction."
​
System Message
We don’t recommend modifying the system message, as doing so opts you out of future updates to the core system message. Use --custom_instructions instead, to add relevant information to the system message. If you must modify the system message, you can do so by using this argument, or by changing a profile file.


Terminal

Python

Profile

Copy

Ask AI
interpreter --system_message "You are Open Interpreter..."
​
Disable Telemetry
Opt out of telemetry.


Terminal

Python

Profile

Copy

Ask AI
interpreter --disable_telemetry
​
Offline
This boolean flag determines whether to enable or disable some offline features like open procedures. Use this in conjunction with the model parameter to set your language model.


Python

Terminal

Profile

Copy

Ask AI
interpreter.offline = True
​
Messages
This property holds a list of messages between the user and the interpreter.

You can use it to restore a conversation:


Copy

Ask AI
interpreter.chat("Hi! Can you print hello world?")

print(interpreter.messages)

# This would output:

# [
#    {
#       "role": "user",
#       "message": "Hi! Can you print hello world?"
#    },
#    {
#       "role": "assistant",
#       "message": "Sure!"
#    }
#    {
#       "role": "assistant",
#       "language": "python",
#       "code": "print('Hello, World!')",
#       "output": "Hello, World!"
#    }
# ]

#You can use this to restore `interpreter` to a previous conversation.
interpreter.messages = messages # A list that resembles the one above
​
User Message Template
A template applied to the User’s message. {content} will be replaced with the user’s message, then sent to the language model.


Python

Profile

Copy

Ask AI
interpreter.user_message_template = "{content} Please send me some code that would be able to answer my question, in the form of ```python\n... the code ...\n``` or ```shell\n... the code ...\n```"
​
Always Apply User Message Template
The boolean flag for whether the User Message Template will be applied to every user message. The default is False which means the template is only applied to the last User message.


Python

Profile

Copy

Ask AI
interpreter.always_apply_user_message_template = False
​
Code Message Template
A template applied to the Computer’s output after running code. {content} will be replaced with the computer’s output, then sent to the language model.


Python

Profile

Copy

Ask AI
interpreter.code_output_template = "Code output: {content}\nWhat does this output mean / what's next (if anything, or are we done)?"
​
Empty Code Message Template
If the computer does not output anything after code execution, this value will be sent to the language model.


Python

Profile

Copy

Ask AI
interpreter.empty_code_output_template = "The code above was executed on my machine. It produced no text output. what's next (if anything, or are we done?)"
​
Code Output Sender
This field determines whether the computer / code output messages are sent as the assistant or as the user. The default is user.


Python

Profile

Copy

Ask AI
interpreter.code_output_sender = "user"
​
Computer
The computer object in interpreter.computer is a virtual computer that the AI controls. Its primary interface/function is to execute code and return the output in real-time.

​
Offline
Running the computer in offline mode will disable some online features, like the hosted Computer API. Inherits from interpreter.offline.


Python

Profile

Copy

Ask AI
interpreter.computer.offline = True
​
Verbose
This is primarily used for debugging interpreter.computer. Inherits from interpreter.verbose.


Python

Profile

Copy

Ask AI
interpreter.computer.verbose = True
​
Emit Images
The emit_images attribute in interpreter.computer controls whether the computer should emit images or not. This is inherited from interpreter.llm.supports_vision.

This is used for multimodel vs. text only models. Running computer.display.view() will return an actual screenshot for multimodal models if emit_images is True. If it’s False, computer.display.view() will return all the text on the screen.

Many other functions of the computer can produce image/text outputs, and this parameter controls that.


Python

Profile

Copy

Ask AI
interpreter.computer.emit_images = True
​
Import Computer API
Include the computer API in the system message. The default is False and won’t import the computer API automatically


Python

Profile

Copy

Ask AI
interpreter.computer.import_computer_api = True

Usage
​
Running Code
The computer itself is separate from Open Interpreter’s core, so you can run it independently:


Copy

Ask AI
from interpreter import interpreter

interpreter.computer.run("python", "print('Hello World!')")
This runs in the same Python instance that interpreter uses, so you can define functions, variables, or log in to services before the AI starts running code:


Copy

Ask AI
interpreter.computer.run("python", "import replicate\nreplicate.api_key='...'")

interpreter.custom_instructions = "Replicate has already been imported."

interpreter.chat("Please generate an image on replicate...") # Interpreter will be logged into Replicate
​
Custom Languages
You also have control over the computer’s languages (like Python, Javascript, and Shell), and can easily append custom languages:

Code Execution
Computer API
The following functions are designed for language models to use in Open Interpreter, currently only supported in OS Mode.

​
Display - View
Takes a screenshot of the primary display.


Copy

Ask AI
interpreter.computer.display.view()
​
Display - Center
Gets the x, y value of the center of the screen.


Copy

Ask AI
x, y = interpreter.computer.display.center()
​
Keyboard - Hotkey
Performs a hotkey on the computer


Copy

Ask AI
interpreter.computer.keboard.hotkey(" ", "command")
​
Keyboard - Write
Writes the text into the currently focused window.


Copy

Ask AI
interpreter.computer.keyboard.write("hello")
​
Mouse - Click
Clicks on the specified coordinates, or an icon, or text. If text is specified, OCR will be run on the screenshot to find the text coordinates and click on it.


Copy

Ask AI
# Click on coordinates
interpreter.computer.mouse.click(x=100, y=100)

# Click on text on the screen
interpreter.computer.mouse.click("Onscreen Text")

# Click on a gear icon
interpreter.computer.mouse.click(icon="gear icon")
​
Mouse - Move
Moves to the specified coordinates, or an icon, or text. If text is specified, OCR will be run on the screenshot to find the text coordinates and move to it.


Copy

Ask AI
# Click on coordinates
interpreter.computer.mouse.move(x=100, y=100)

# Click on text on the screen
interpreter.computer.mouse.move("Onscreen Text")

# Click on a gear icon
interpreter.computer.mouse.move(icon="gear icon")
​
Mouse - Scroll
Scrolls the mouse a specified number of pixels.


Copy

Ask AI
# Scroll Down
interpreter.computer.mouse.scroll(-10)

# Scroll Up
interpreter.computer.mouse.scroll(10)
​
Clipboard - View
Returns the contents of the clipboard.


Copy

Ask AI
interpreter.computer.clipboard.view()
​
OS - Get Selected Text
Get the selected text on the screen.


Copy

Ask AI
interpreter.computer.os.get_selected_text()
​
Mail - Get
Retrieves the last number emails from the inbox, optionally filtering for only unread emails. (Mac only)


Copy

Ask AI
interpreter.computer.mail.get(number=10, unread=True)
​
Mail - Send
Sends an email with the given parameters using the default mail app. (Mac only)


Copy

Ask AI
interpreter.computer.mail.send("john@email.com", "Subject", "Body", ["path/to/attachment.pdf", "path/to/attachment2.pdf"])
​
Mail - Unread Count
Retrieves the count of unread emails in the inbox. (Mac only)


Copy

Ask AI
interpreter.computer.mail.unread_count()
​
SMS - Send
Send a text message using the default SMS app. (Mac only)


Copy

Ask AI
interpreter.computer.sms.send("2068675309", "Hello from Open Interpreter!")
​
Contacts - Get Phone Number
Returns the phone number of a contact name. (Mac only)


Copy

Ask AI
interpreter.computer.contacts.get_phone_number("John Doe")
​
Contacts - Get Email Address
Returns the email of a contact name. (Mac only)


Copy

Ask AI
interpreter.computer.contacts.get_phone_number("John Doe")
​
Calendar - Get Events
Fetches calendar events for the given date or date range from all calendars. (Mac only)


Copy

Ask AI
interpreter.computer.calendar.get_events(start_date=datetime, end_date=datetime)
​
Calendar - Create Event
Creates a new calendar event. Uses first calendar if none is specified (Mac only)


Copy

Ask AI
interpreter.computer.calendar.create_event(title="Title", start_date=datetime, end_date=datetime, location="Location", notes="Notes", calendar="Work")
​
Calendar - Delete Event
Delete a specific calendar event. (Mac only)


Copy

Ask AI
interpreter.computer.calendar.delete_event(event_title="Title", start_date=datetime,

Code Execution
Custom Languages
You can add or edit the programming languages that Open Interpreter’s computer runs.

In this example, we’ll swap out the python language for a version of python that runs in the cloud. We’ll use E2B to do this.

(E2B is a secure, sandboxed environment where you can run arbitrary code.)

First, get an API key here, and set it:


Copy

Ask AI
import os
os.environ["E2B_API_KEY"] = "<your_api_key_here>"
Then, define a custom language for Open Interpreter. The class name doesn’t matter, but we’ll call it PythonE2B:


Copy

Ask AI
import e2b

class PythonE2B:
    """
    This class contains all requirements for being a custom language in Open Interpreter:

    - name (an attribute)
    - run (a method)
    - stop (a method)
    - terminate (a method)

    You can use this class to run any language you know how to run, or edit any of the official languages (which also conform to this class).

    Here, we'll use E2B to power the `run` method.
    """

    # This is the name that will appear to the LLM.
    name = "python"

    # Optionally, you can append some information about this language to the system message:
    system_message = "# Follow this rule: Every Python code block MUST contain at least one print statement."

    # (E2B isn't a Jupyter Notebook, so we added ^ this so it would print things,
    # instead of putting variables at the end of code blocks, which is a Jupyter thing.)

    def run(self, code):
        """Generator that yields a dictionary in LMC Format."""

        # Run the code on E2B
        stdout, stderr = e2b.run_code('Python3', code)

        # Yield the output
        yield {
            "type": "console", "format": "output",
            "content": stdout + stderr # We combined these arbitrarily. Yield anything you'd like!
        }

    def stop(self):
        """Stops the code."""
        # Not needed here, because e2b.run_code isn't stateful.
        pass

    def terminate(self):
        """Terminates the entire process."""
        # Not needed here, because e2b.run_code isn't stateful.
        pass

# (Tip: Do this before adding/removing languages, otherwise OI might retain the state of previous languages:)
interpreter.computer.terminate()

# Give Open Interpreter its languages. This will only let it run PythonE2B:
interpreter.computer.languages = [PythonE2B]

# Try it out!
interpreter.chat("What's 349808*38490739?")

Protocols
LMC Messages
To support the incoming Language Model Computer architecture, we extend OpenAI’s messages format to include additional information, and a new role called computer:


Copy

Ask AI
# The user sends a message.
{"role": "user", "type": "message", "content": "What's 2380*3875?"}

# The assistant runs some code.
{"role": "assistant", "type": "code", "format": "python", "content": "2380*3875"}

# The computer responds with the result of the code.
{"role": "computer", "type": "console", "format": "output", "content": "9222500"}

# The assistant sends a message.
{"role": "assistant", "type": "message", "content": "The result of multiplying 2380 by 3875 is 9222500."}
​
Anatomy
Each message in the LMC architecture has the following parameters (format is only present for some types):


Copy

Ask AI
{
  "role": "<role>",       # Who is sending the message.
  "type": "<type>",       # What kind of message is being sent.
  "format": "<format>"    # Some types need to be further specified, so they optionally use this parameter.
  "content": "<content>", # What the message says.
}
Parameter	Description
role	The sender of the message.
type	The kind of message being sent.
content	The actual content of the message.
format	The format of the content (optional).
​
Roles
Role	Description
user	The individual interacting with the system.
assistant	The language model.
computer	The system that executes the language model’s commands.
​
Possible Message Types / Formats
Any role can produce any of the following formats, but we’ve included a Common Roles column to give you a sense of the message type’s usage.

Type	Format	Content Description	Common Roles
message	None	A text-only message.	user, assistant
console	active_line	The active line of code (from the most recent code block) that’s executing.	computer
console	output	Text output resulting from print() statements in Python, console.log() statements in Javascript, etc. This includes errors.	computer
image	base64	A base64 image in PNG format (default)	user, computer
image	base64.png	A base64 image in PNG format	user, computer
image	base64.jpeg	A base64 image in JPEG format	user, computer
image	path	A path to an image.	user, computer
code	html	HTML code that should be executed.	assistant, computer
code	javascript	JavaScript code that should be executed.	assistant, computer
code	python	Python code that should be executed.	assistant
code	r	R code that should be executed.	assistant
code	applescript	AppleScript code that should be executed.	assistant
code	shell	Shell code that should be executed.	assistant
audio	wav	audio in wav format for websocket.	user

Guides
Basic Usage
Interactive demo
Try Open Interpreter without installing anything on your computer

Example voice interface
An example implementation of Open Interpreter’s streaming capabilities

​
Interactive Chat
To start an interactive chat in your terminal, either run interpreter from the command line or interpreter.chat() from a .py file.


Terminal

Python

Copy

Ask AI
interpreter
​
Programmatic Chat
For more precise control, you can pass messages directly to .chat(message) in Python:


Copy

Ask AI
interpreter.chat("Add subtitles to all videos in /videos.")

# ... Displays output in your terminal, completes task ...

interpreter.chat("These look great but can you make the subtitles bigger?")

# ...
​
Start a New Chat
In your terminal, Open Interpreter behaves like ChatGPT and will not remember previous conversations. Simply run interpreter to start a new chat.

In Python, Open Interpreter remembers conversation history. If you want to start fresh, you can reset it.


Terminal

Python

Copy

Ask AI
interpreter
​
Save and Restore Chats
In your terminal, Open Interpreter will save previous conversations to <your application directory>/Open Interpreter/conversations/.

You can resume any of them by running --conversations. Use your arrow keys to select one , then press ENTER to resume it.

In Python, interpreter.chat() returns a List of messages, which can be used to resume a conversation with interpreter.messages = messages.


Terminal

Python

Copy

Ask AI
interpreter --conversations
​
Configure Default Settings
We save default settings to the default.yaml profile which can be opened and edited by running the following command:


Copy

Ask AI
interpreter --profiles
You can use this to set your default language model, system message (custom instructions), max budget, etc.

Note: The Python library will also inherit settings from the default profile file. You can change it by running interpreter --profiles and editing default.yaml.

​
Customize System Message
In your terminal, modify the system message by editing your configuration file as described here.

In Python, you can inspect and configure Open Interpreter’s system message to extend its functionality, modify permissions, or give it more context.


Copy

Ask AI
interpreter.system_message += """
Run shell commands with -y so the user doesn't have to confirm them.
"""
print(interpreter.system_message)
​
Change your Language Model
Open Interpreter uses LiteLLM to connect to language models.

You can change the model by setting the model parameter:


Copy

Ask AI
interpreter --model gpt-3.5-turbo
interpreter --model claude-2
interpreter --model command-nightly
In Python, set the model on the object:


Copy

Ask AI
interpreter.llm.model = "gpt-3.5-turbo"
Find the appropriate “model” string for your language model here.

Guides
Running Locally
Open Interpreter can be run fully locally.

Users need to install software to run local LLMs. Open Interpreter supports multiple local model providers such as Ollama, Llamafile, Jan, and LM Studio.

Local models perform better with extra guidance and direction. You can improve performance for your use-case by creating a new Profile.

​
Terminal Usage
​
Local Explorer
A Local Explorer was created to simplify the process of using OI locally. To access this menu, run the command interpreter --local.

Select your chosen local model provider from the list of options.

Most providers will require the user to state the model they are using. Provider specific instructions are shown to the user in the menu.

​
Custom Local
If you want to use a provider other than the ones listed, you will set the --api_base flag to set a custom endpoint.

You will also need to set the model by passing in the --model flag to select a model.


Copy

Ask AI
interpreter --api_base "http://localhost:11434" --model ollama/codestral
Other terminal flags are explained in Settings.

​
Python Usage
In order to have a Python script use Open Interpreter locally, some fields need to be set


Copy

Ask AI
from interpreter import interpreter

interpreter.offline = True
interpreter.llm.model = "ollama/codestral"
interpreter.llm.api_base = "http://localhost:11434"

interpreter.chat("how many files are on my desktop?")
​
Helpful settings for local models
Local models benefit from more coercion and guidance. This verbosity of adding extra context to messages can impact the conversational experience of Open Interpreter. The following settings allow templates to be applied to messages to improve the steering of the language model while maintaining the natural flow of conversation.

interpreter.user_message_template allows users to have their message wrapped in a template. This can be helpful steering a language model to a desired behaviour without needing the user to add extra context to their message.

interpreter.always_apply_user_message_template has all user messages to be wrapped in the template. If False, only the last User message will be wrapped.

interpreter.code_output_template wraps the output from the computer after code is run. This can help with nudging the language model to continue working or to explain outputs.

interpreter.empty_code_output_template is the message that is sent to the language model if code execution results in no output.

Other configuration settings are explained in Settings.

Guides
Profiles

Profiles are a powerful way to customize your instance of Open Interpreter.

Profiles are Python files that configure Open Interpreter. A wide range of fields from the model to the context window to the message templates can be configured in a Profile. This allows you to save multiple variations of Open Interpreter to optimize for your specific use-cases.

You can access your Profiles by running interpreter --profiles. This will open the directory where all of your Profiles are stored.

If you want to make your own profile, start with the Template Profile.

To apply a Profile to an Open Interpreter session, you can run interpreter --profile <name>

​
Example Python Profile

Copy

Ask AI
from interpreter import interpreter

interpreter.os = True
interpreter.llm.supports_vision = True

interpreter.llm.model = "gpt-4o"

interpreter.llm.supports_functions = True
interpreter.llm.context_window = 110000
interpreter.llm.max_tokens = 4096
interpreter.auto_run = True
interpreter.loop = True
​
Example YAML Profile
Make sure YAML profile version is set to 0.2.5

Copy

Ask AI
llm:
  model: "gpt-4-o"
  temperature: 0
  # api_key: ...  # Your API key, if the API requires it
  # api_base: ...  # The URL where an OpenAI-compatible server is running to handle LLM API requests

# Computer Settings
computer:
  import_computer_api: True # Gives OI a helpful Computer API designed for code interpreting language models

# Custom Instructions
custom_instructions: ""  # This will be appended to the system message

# General Configuration
auto_run: False  # If True, code will run without asking for confirmation
offline: False  # If True, will disable some online features like checking for updates

version: 0.2.5 # Configuration file version (do not modify)

Guides
Streaming Response
You can stream messages, code, and code outputs out of Open Interpreter by setting stream=True in an interpreter.chat(message) call.


Copy

Ask AI
for chunk in interpreter.chat("What's 34/24?", stream=True, display=False):
  print(chunk)

Copy

Ask AI
{"role": "assistant", "type": "code", "format": "python", "start": True}
{"role": "assistant", "type": "code", "format": "python", "content": "34"}
{"role": "assistant", "type": "code", "format": "python", "content": " /"}
{"role": "assistant", "type": "code", "format": "python", "content": " "}
{"role": "assistant", "type": "code", "format": "python", "content": "24"}
{"role": "assistant", "type": "code", "format": "python", "end": True}

{"role": "computer", "type": "confirmation", "format": "execution", "content": {"type": "code", "format": "python", "content": "34 / 24"}},

{"role": "computer", "type": "console", "start": True}
{"role": "computer", "type": "console", "format": "active_line", "content": "1"}
{"role": "computer", "type": "console", "format": "output", "content": "1.4166666666666667\n"}
{"role": "computer", "type": "console", "format": "active_line", "content": None},
{"role": "computer", "type": "console", "end": True}

{"role": "assistant", "type": "message", "start": True}
{"role": "assistant", "type": "message", "content": "The"}
{"role": "assistant", "type": "message", "content": " result"}
{"role": "assistant", "type": "message", "content": " of"}
{"role": "assistant", "type": "message", "content": " the"}
{"role": "assistant", "type": "message", "content": " division"}
{"role": "assistant", "type": "message", "content": " "}
{"role": "assistant", "type": "message", "content": "34"}
{"role": "assistant", "type": "message", "content": "/"}
{"role": "assistant", "type": "message", "content": "24"}
{"role": "assistant", "type": "message", "content": " is"}
{"role": "assistant", "type": "message", "content": " approximately"}
{"role": "assistant", "type": "message", "content": " "}
{"role": "assistant", "type": "message", "content": "1"}
{"role": "assistant", "type": "message", "content": "."}
{"role": "assistant", "type": "message", "content": "42"}
{"role": "assistant", "type": "message", "content": "."}
{"role": "assistant", "type": "message", "end": True}
Note: Setting display=True won’t change the behavior of the streaming response, it will just render a display in your terminal.

​
Anatomy
Each chunk of the streamed response is a dictionary, that has a “role” key that can be either “assistant” or “computer”. The “type” key describes what the chunk is. The “content” key contains the actual content of the chunk.

Every ‘message’ is made up of chunks, and begins with a “start” chunk, and ends with an “end” chunk. This helps you parse the streamed response into messages.

Let’s break down each part of the streamed response.

​
Code
In this example, the LLM decided to start writing code first. It could have decided to write a message first, or to only write code, or to only write a message.

Every streamed chunk of type “code” has a format key that specifies the language. In this case it decided to write python.

This can be any language defined in our languages directory.


Copy

Ask AI

{"role": "assistant", "type": "code", "format": "python", "start": True}

Then, the LLM decided to write some code. The code is sent token-by-token:


Copy

Ask AI

{"role": "assistant", "type": "code", "format": "python", "content": "34"}
{"role": "assistant", "type": "code", "format": "python", "content": " /"}
{"role": "assistant", "type": "code", "format": "python", "content": " "}
{"role": "assistant", "type": "code", "format": "python", "content": "24"}

When the LLM finishes writing code, it will send an “end” chunk:


Copy

Ask AI

{"role": "assistant", "type": "code", "format": "python", "end": True}

​
Code Output
After the LLM finishes writing a code block, Open Interpreter will attempt to run it.

Before it runs it, the following chunk is sent:


Copy

Ask AI

{"role": "computer", "type": "confirmation", "format": "execution", "content": {"type": "code", "language": "python", "code": "34 / 24"}}

If you check for this object, you can break (or get confirmation) before executing the code.


Copy

Ask AI
# This example asks the user before running code

for chunk in interpreter.chat("What's 34/24?", stream=True):
    if "executing" in chunk:
        if input("Press ENTER to run this code.") != "":
            break
While the code is being executed, you’ll receive the line of code that’s being run:


Copy

Ask AI
{"role": "computer", "type": "console", "format": "active_line", "content": "1"}
We use this to highlight the active line of code on our UI, which keeps the user aware of what Open Interpreter is doing.

You’ll then receive its output, if it produces any:


Copy

Ask AI
{"role": "computer", "type": "console", "format": "output", "content": "1.4166666666666667\n"}
When the code is finished executing, this flag will be sent:


Copy

Ask AI
{"role": "computer", "type": "console", "end": True}
​
Message
Finally, the LLM decided to write a message. This is streamed token-by-token as well:


Copy

Ask AI
{"role": "assistant", "type": "message", "start": True}
{"role": "assistant", "type": "message", "content": "The"}
{"role": "assistant", "type": "message", "content": " result"}
{"role": "assistant", "type": "message", "content": " of"}
{"role": "assistant", "type": "message", "content": " the"}
{"role": "assistant", "type": "message", "content": " division"}
{"role": "assistant", "type": "message", "content": " "}
{"role": "assistant", "type": "message", "content": "34"}
{"role": "assistant", "type": "message", "content": "/"}
{"role": "assistant", "type": "message", "content": "24"}
{"role": "assistant", "type": "message", "content": " is"}
{"role": "assistant", "type": "message", "content": " approximately"}
{"role": "assistant", "type": "message", "content": " "}
{"role": "assistant", "type": "message", "content": "1"}
{"role": "assistant", "type": "message", "content": "."}
{"role": "assistant", "type": "message", "content": "42"}
{"role": "assistant", "type": "message", "content": "."}
{"role": "assistant", "type": "message", "end": True}
For an example in JavaScript on how you might process these streamed chunks, see the migration guide

Guides
Advanced Terminal Usage
Magic commands can be used to control the interpreter’s behavior in interactive mode:

%% [shell commands, like ls or cd]: Run commands in Open Interpreter’s shell instance
%verbose [true/false]: Toggle verbose mode. Without arguments or with ‘true’, it enters verbose mode. With ‘false’, it exits verbose mode.
%reset: Reset the current session.
%undo: Remove previous messages and its response from the message history.
%save_message [path]: Saves messages to a specified JSON path. If no path is provided, it defaults to ‘messages.json’.
%load_message [path]: Loads messages from a specified JSON path. If no path is provided, it defaults to ‘messages.json’.
%tokens [prompt]: EXPERIMENTAL: Calculate the tokens used by the next request based on the current conversation’s messages and estimate the cost of that request; optionally provide a prompt to also calculate the tokens used by that prompt and the total amount of tokens that will be sent with the next request.
%info: Show system and interpreter information.
%help: Show this help message.
%jupyter: Export the current session to a Jupyter notebook file (.ipynb) to the Downloads folder.
%markdown [path]: Export the conversation to a specified Markdown path. If no path is provided, it will be saved to the Downloads folder with a generated conversation name.

Multiple Instances
To create multiple instances, use the base class, OpenInterpreter:


Copy

Ask AI
from interpreter import OpenInterpreter

agent_1 = OpenInterpreter()
agent_1.system_message = "This is a separate instance."

agent_2 = OpenInterpreter()
agent_2.system_message = "This is yet another instance."
For fun, you could make these instances talk to eachother:


Copy

Ask AI
def swap_roles(messages):
    for message in messages:
        if message['role'] == 'user':
            message['role'] = 'assistant'
        elif message['role'] == 'assistant':
            message['role'] = 'user'
    return messages

agents = [agent_1, agent_2]

# Kick off the conversation
messages = [{"role": "user", "message": "Hello!"}]

while True:
    for agent in agents:
        messages = agent.chat(messages)
        messages = swap_roles(messages)

OS Mode
OS mode is a highly experimental mode that allows Open Interpreter to control the operating system visually through the mouse and keyboard. It provides a multimodal LLM like GPT-4V with the necessary tools to capture screenshots of the display and interact with on-screen elements such as text and icons. It will try to use the most direct method to achieve the goal, like using spotlight on Mac to open applications, and using query parameters in the URL to open websites with additional information.

OS mode is a work in progress, if you have any suggestions or experience issues, please reach out on our Discord.

To enable OS Mode, run the interpreter with the --os flag:


Copy

Ask AI
interpreter --os
Please note that screen recording permissions must be enabled for your terminal application for OS mode to work properly to work.

OS mode does not currently support multiple displays.

Ollama
Ollama is an easy way to get local language models running on your computer through a command-line interface.

To run Ollama with Open interpreter:

Download Ollama for your platform from here.

Open the installed Ollama application, and go through the setup, which will require your password.

Now you are ready to download a model. You can view all available models here. To download a model, run:


Copy

Ask AI
ollama run <model-name>
It will likely take a while to download, but once it does, we are ready to use it with Open Interpreter. You can either run interpreter --local to set it up interactively in the terminal, or do it manually:

Terminal

Python

Copy

Ask AI
interpreter --model ollama/<model-name>
For any future runs with Ollama, ensure that the Ollama server is running. If using the desktop application, you can check to see if the Ollama menu bar item is active.

If Ollama is producing strange output, make sure to update to the latest version

Local Providers
LlamaFile
The easiest way to get started with local models in Open Interpreter is to run interpreter --local in the terminal, select LlamaFile, then go through the interactive set up process. This will download the model and start the server for you. If you choose to do it manually, you can follow the instructions below.

To use LlamaFile manually with Open Interpreter, you’ll need to download the model and start the server by running the file in the terminal. You can do this with the following commands:


Copy

Ask AI
# Download Mixtral

wget https://huggingface.co/jartine/Mixtral-8x7B-v0.1.llamafile/resolve/main/mixtral-8x7b-instruct-v0.1.Q5_K_M-server.llamafile

# Make it an executable

chmod +x mixtral-8x7b-instruct-v0.1.Q5_K_M-server.llamafile

# Start the server

./mixtral-8x7b-instruct-v0.1.Q5_K_M-server.llamafile

# In a separate terminal window, run OI and point it at the llamafile server

interpreter --api_base https://localhost:8080/v1
Please note that if you are using a Mac with Apple Silicon, you’ll need to have Xcode installed.

Local Providers
Custom Endpoint
Simply set api_base to any OpenAI compatible server:


Terminal

Python

Copy

Ask AI
interpreter --api_base <custom_endpoint>

Best Practices
Most settings — like model architecture and GPU offloading — can be adjusted via your LLM providers like LM Studio.

However, max_tokens and context_window should be set via Open Interpreter.

For local mode, smaller context windows will use less RAM, so we recommend trying a much shorter window (~1000) if it’s is failing or if it’s slow.


Terminal

Python

Copy

Ask AI
interpreter --local --max_tokens 1000 --context_window 3000

anguage Models
Custom Models
In addition to hosted and local language models, Open Interpreter also supports custom models.

As long as your system can accept an input and stream an output (and can be interacted with via a Python generator) it can be used as a language model in Open Interpreter.

Simply replace the OpenAI-compatible completions function in your language model with one of your own:


Copy

Ask AI
def custom_language_model(messages, model, stream, max_tokens):
    """
    OpenAI-compatible completions function (this one just echoes what the user said back).
    To make it OpenAI-compatible and parsable, `choices` has to be the root property.
    The property `delta` is used to signify streaming.
    """
    users_content = messages[-1].get("content") # Get last message's content

    for character in users_content:
        yield {"choices": [{"delta": {"content": character}}]}

# Tell Open Interpreter to power the language model with this function

interpreter.llm.completions = custom_language_model
Then, set the following settings:


Copy

Ask AI
interpreter.llm.context_window = 2000 # In tokens
interpreter.llm.max_tokens = 1000 # In tokens
interpreter.llm.supports_vision = False # Does this completions endpoint accept images?
interpreter.llm.supports_functions = False # Does this completions endpoint accept/return function calls?
And start using it:


Copy

Ask AI
interpreter.chat("Hi!") # Returns/displays "Hi!" character by character

Integrations
E2B
E2B is a secure, sandboxed environment where you can run arbitrary code.

To build this integration, you just need to replace Open Interpreter’s python (which runs locally) with a python that runs on E2B.

First, get an API key here, and set it:


Copy

Ask AI
import os
os.environ["E2B_API_KEY"] = "<your_api_key_here>"
Then, define a custom language for Open Interpreter. The class name doesn’t matter, but we’ll call it PythonE2B:


Copy

Ask AI
import e2b

class PythonE2B:
    """
    This class contains all requirements for being a custom language in Open Interpreter:

    - name (an attribute)
    - run (a method)
    - stop (a method)
    - terminate (a method)

    Here, we'll use E2B to power the `run` method.
    """

    # This is the name that will appear to the LLM.
    name = "python"

    # Optionally, you can append some information about this language to the system message:
    system_message = "# Follow this rule: Every Python code block MUST contain at least one print statement."

    # (E2B isn't a Jupyter Notebook, so we added ^ this so it would print things,
    # instead of putting variables at the end of code blocks, which is a Jupyter thing.)

    def run(self, code):
        """Generator that yields a dictionary in LMC Format."""

        # Run the code on E2B
        stdout, stderr = e2b.run_code('Python3', code)

        # Yield the output
        yield {
            "type": "console", "format": "output",
            "content": stdout + stderr # We combined these arbitrarily. Yield anything you'd like!
        }

    def stop(self):
        """Stops the code."""
        # Not needed here, because e2b.run_code isn't stateful.
        pass

    def terminate(self):
        """Terminates the entire process."""
        # Not needed here, because e2b.run_code isn't stateful.
        pass

# (Tip: Do this before adding/removing languages, otherwise OI might retain the state of previous languages:)
interpreter.computer.terminate()

# Give Open Interpreter its languages. This will only let it run PythonE2B:
interpreter.computer.languages = [PythonE2B]

# Try it out!
interpreter.chat("What's 349808*38490739?")

Safety
Introduction
Safety is a top priority for us at Open Interpreter. Running LLM generated code on your computer is inherently risky, and we have taken steps to make it as safe as possible. One of the primary safety ‘mechanisms’, is the alignment of the LLM itself. GPT-4 refuses to run dangerous code like rm -rf /, it understands what that command will do, and won’t let you footgun yourself. This is less applicable when running local models like Mistral, that have little or no alignment, making our other safety measures more important.

​
Safety Measures
Safe mode enables code scanning, as well as the ability to scan packages with guarddog with a simple change to the system message. See the safe mode docs for more information.

Requiring confirmation with the user before the code is actually run. This is a simple measure that can prevent a lot of accidents. It exists as another layer of protection, but can be disabled with the --auto-run flag if you wish.

Sandboxing code execution. Open Interpreter can be run in a sandboxed environment using Docker. This is a great way to run code without worrying about it affecting your system. Docker support is currently experimental, but we are working on making it a core feature of Open Interpreter. Another option for sandboxing is E2B, which overrides the default python language with a sandboxed, hosted version of python through E2B. Follow this guide to set it up.

​
Notice

Safety
Isolation
Isolating Open Interpreter from your system is helpful to prevent security mishaps. By running it in a separate process, you can ensure that actions taken by Open Interpreter will not directly affect your system. This is by far the safest way to run Open Interpreter, although it can be limiting based on your use case.

If you wish to sandbox Open Interpreter, we have two primary methods of doing so: Docker and E2B.

​
Docker
Docker is a containerization technology that allows you to run an isolated Linux environment on your system. This allows you to run Open Interpreter in a container, which completely isolates it from your system. All code execution is done in the container, and the container is not able to access your system. Docker support is currently experimental, and we are working on integrating it as a core feature of Open Interpreter.

Follow these instructions to get it running.

​
E2B
E2B is a cloud-based platform for running sandboxed code environments, designed for use by AI agents. You can override the default python language in Open Interpreter to use E2B, and it will automatically run the code in a cloud-sandboxed environment. You will need an E2B account to use this feature. It’s worth noting that this will only sandbox python code, other languages like shell and JavaScript will still be run on your system.

Follow these instructions to get it running.

Safety
Safe Mode
​
Safe Mode
⚠️ Safe mode is experimental and does not provide any guarantees of safety or security.

Open Interpreter is working on providing an experimental safety toolkit to help you feel more confident running the code generated by Open Interpreter.

Install Open Interpreter with the safety toolkit dependencies as part of the bundle:


Copy

Ask AI
pip install open-interpreter[safe]
Alternatively, you can install the safety toolkit dependencies separately in your virtual environment:


Copy

Ask AI
pip install semgrep
​
Features
No Auto Run: Safe mode disables the ability to automatically execute code
Code Scanning: Scan generated code for vulnerabilities with semgrep
​
Enabling Safe Mode
You can enable safe mode by passing the --safe flag when invoking interpreter or by configuring safe_mode in your config file.

The safe mode setting has three options:

off: disables the safety toolkit (default)
ask: prompts you to confirm that you want to scan code
auto: automatically scans code
​
Example Config:

Copy

Ask AI
model: gpt-4
temperature: 0
verbose: false
safe_mode: ask
​
Roadmap
Some upcoming features that enable even more safety:

Execute code in containers
​
Tips & Tricks
You can adjust the custom_instructions in your config file to include instructions for the model to scan packages with guarddog before installing them.


Copy

Ask AI
model: gpt-4
verbose: false
safe_mode: ask
system_message: |
  # normal system message here
  BEFORE INSTALLING ANY PACKAGES WITH pip OR npm YOU MUST SCAN THEM WITH `guarddog` F

  Safety
Best Practices
LLM’s are not perfect. They can make mistakes, they can be tricked into doing things that they shouldn’t, and they are capable of writing unsafe code. This page will help you understand how to use these LLM’s safely.

​
Best Practices
Avoid asking it to perform potentially risky tasks. This seems obvious, but it’s the number one way to prevent safety mishaps.

Run it in a sandbox. This is the safest way to run it, as it completely isolates the code it runs from the rest of your system.

Use trusted models. Yes, Open Interpreter can be configured to run pretty much any text-based model on huggingface. But it does not mean it’s a good idea to run any random model you find. Make sure you trust the models you’re using. If you’re not sure, run it in a sandbox. Nefarious LLM’s are becoming a real problem, and they are not going away anytime soon.

Local models are fun! But GPT-4 is probably your safest bet. OpenAI has their models aligned in a major way. It will outperform the local models, and it will generally refuse to run unsafe code, as it truly understands that the code it writes could be run. It has a pretty good idea what unsafe code looks like, and will refuse to run code like rm -rf / that would delete your entire disk, for example.

The —safe_mode argument is your friend. It enables code scanning, and can use guarddog to identify malicious PyPi and npm packages. It’s not a perfect solution, but it’s a great start.

Telemetry
Introduction
Open Interpreter contains a telemetry feature that collects anonymous usage information.

We use this information to help us understand how OI is used, to help us prioritize work on new features and bug fixes, and to help us improve OI’s performance and stability.

​
Opting out
If you prefer to opt out of telemetry, you can do this in two ways.

​
Python
Set disable_telemetry to true on the interpreter object:


Copy

Ask AI
from interpreter import interpreter
interpreter.disable_telemetry = True
​
Terminal
Use the --disable_telemetry flag:


Copy

Ask AI
interpreter --disable_telemetry
​
Profile
Set disable_telemetry to true. This will persist to future terminal sessions:


Copy

Ask AI
disable_telemetry: true
​
Environment Variables
Set DISABLE_TELEMETRY to true in your shell or server environment.

If you are running Open Interpreter on your local computer with docker-compose you can set this value in an .env file placed in the same directory as the docker-compose.yml file:


Copy

Ask AI
DISABLE_TELEMETRY=true
​
What do you track?
We will only track usage details that help us make product decisions, specifically:

Open Interpreter version and environment (i.e whether or not it’s running in Python / a terminal)
When interpreter.chat is run, in what mode (e.g --os mode), and the type of the message being passed in (e.g None, str, or list)
Exceptions that occur within Open Interpreter (not tracebacks)
We do not collect personally-identifiable or sensitive information, such as: usernames, hostnames, file names, environment variables, or hostnames of systems being tested.

To view the list of events we track, you may reference the code

​
Where is telemetry information stored?
We use Posthog to store and visualize telemetry data.