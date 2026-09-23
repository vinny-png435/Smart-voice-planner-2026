from kivy.app import App
from kivy. uix . boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix. button import Button
from kivy.uix. textinput import TextInput
from kivy.clock import Clock


class SmartVoiceApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        title = Label(text = "Smart Voice Planner", font_size=30)
        add_button = Button(text="Add New Task", font_size=22)
        add_button.bind(on_press=self.add_new_task)
        self.layout.add_widget(title)
        self.layout.add_widget(add_button)
        return self.layout
    def add_new_task(self,instance):
      print("Add New Task Clicked")
      self.task_input = TextInput(hint_text="Enter Task Name",multiline=False,font_size=22)
      self.time_input = TextInput(hint_text="Enter Time (e.g. 9:00 AM)", multiline=False, font_size=22)
      save_button = Button(text="Save Task", font_size=22)
      save_button.bind(on_press=self.save_task)
      self.layout.add_widget(self.task_input)
      self.layout.add_widget(self.time_input)
      self.layout.add_widget(save_button)
    async def make_task_voice(self,text):
         from gtts import gTTS
         output_file="task_voice.mp3"
         tts = gTTS(text=text, lang="te", slow=True)
         tts.save(output_file)
         return output_file
    def speak_task(self,task_name,task_time):
        import asyncio
        from kivy.core.audio import SoundLoader
        print("SPEAK TASK STARTED")
        print("TASK:", task_name)

        try:
             voice_file=asyncio.run(self.make_task_voice(task_name))
             print("VOICE FILE CREATED:", voice_file)
             sound = SoundLoader.load(voice_file)
             if sound:
                print("SOUND LOADED")
                sound.play()
                print("VOICE PLAY COMMAND SENT")
             else:
                print("SOUND LOAD FAILED")

        except Exception as e:
              print("VOICE ERROR:", e)
        
    def save_task(self,instance):
      task_name = self.task_input.text
      task_time = self.time_input.text
      task_label= Label(text=f"{task_time}-{task_name}", font_size=22)
      self.layout.add_widget(task_label)

      from datetime import datetime

      current_time=datetime.now().replace(second=0,microsecond=0)
      target_time=datetime.strptime(task_time,"%I:%M %p")
      target_time=target_time.replace(year=current_time.year, month=current_time.month,day=current_time.day)
      delay=(target_time-current_time).total_seconds()

   

      if delay<0:
         delay+=24*60*60

      Clock.schedule_once(lambda dt:self.speak_task(task_name,task_time),delay)
      print("TASK SCHEDULED", delay)
      self.task_input.text=" "
      self.time_input.text=" "
SmartVoiceApp().run()