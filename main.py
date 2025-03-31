import requests
import gradio as gr
import time
URL= 'https://public-api.beatoven.ai//api/v1'
api='f1rwEE_1iT5SdOrt-OQnTA'
def generate_music_track(mood,duration):
    url = URL+'/tracks'
    headers = {
        "Authorization": f"Bearer {api}",
        "Content-Type": "application/json"
    }
    txt=''
    if mood=='happy':
        txt='Energetic A lively and joyful pop track with a catchy rhythm.'
    elif mood=='sad':
        txt='A soft piano ballad evoking deep emotions and reflection'
    elif mood=='party':
        txt='High-energy EDM track with pulsating beats for the dance floor'
    elif mood=='motivation':
        txt='Epic orchestral composition with rising strings and percussion for inspiration'
    elif mood=='Unknown':
        txt='Abstract electronic music with unpredictable rhythms and textures.'
    payload = {
        "prompt": {"text": f'{duration} seconds {txt} track'}
    }

    response = requests.post(url, headers=headers, json=payload)  # Raise an exception for bad status codes (4xx or 5xx)
    music = response.json()
    #print(music)
    return music
def music_compose(track):
    url=URL+f'/tracks/compose/{track}'
    headers = {
        "Authorization": f"Bearer {api}",
        "Content-Type": "application/json"
    }
    payload ={
            "format": "mp3",
            "looping": True
        }
    response = requests.post(url, headers=headers, json=payload)  # Raise an exception for bad status codes (4xx or 5xx)
    music = response.json()
    # print(music)
    return music
def music(task):
    a=task
    url=URL+f'/tasks/{a}'
    headers = {
        "Authorization": f"Bearer {api}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    #print(response.json())
    if response.status_code == 200:
        result = response.json()
        #print(result)
        return result
    else:
        return None
def gen_music(mood,duration,res):
    track_url = res["meta"]["track_url"]  # Extract the track URL
    if track_url:
        music_response = requests.get(track_url)
        filename = "generated_music.mp3"
        with open(filename, "wb") as f:
            f.write(music_response.content)
        file_path =filename
        if "Error" in file_path:
            return file_path
        else:
            return file_path
def music_interface(mood, duration):
    mood=mood
    duration=duration
    track=generate_music_track(mood,duration)
    t1=track['tracks']
    task=music_compose(t1[0])
    print(task)
    res=''
    b=True
    #res=music(task['task_id'])
    #print(res)
    while b:
        res=music(task['task_id'])
        if res['status']!='composing' and res['status']!='running':
            b=False
            break
        #print(res)
        time.sleep(30)
    #print(task)
    file_path=gen_music(mood,duration,res)
    return file_path
l=['happy','sad','party','motivation','Unknown']
interface = gr.Interface(
    fn=music_interface,
    inputs=[
        gr.Dropdown(l, type='index'),
        gr.Slider(10, 300, step=10, label="Duration (seconds)"),
    ],
    outputs="audio",
    title="Mood-Based Music Generator",
    description="Generate and play AI-composed music based on your mood."
)
if __name__ == "__main__":
    interface.launch()
