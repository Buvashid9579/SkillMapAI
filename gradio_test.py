import gradio as gr

def test(skill, location):
    print("Received:", repr(skill), repr(location))
    return f"{skill} - {location}"

with gr.Blocks() as demo:

    skill = gr.Textbox(label="Skill")
    location = gr.Textbox(label="Location")

    btn = gr.Button("Test")

    out = gr.Textbox()

    btn.click(
        fn=test,
        inputs=[skill, location],
        outputs=out
    )

demo.launch()