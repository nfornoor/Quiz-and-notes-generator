import streamlit as st
from api_calling import audio_generator, note_generator, quiz_generator
from PIL import Image


st.title("Note Summary and Quize Generator")
st.markdown("Upload upto 3 images to generate note Summary and Quizes")
st.divider()
with st.sidebar:
    #image
    st.header("Controls")
    images = st.file_uploader(
        "Upload your images here",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="file_uploader",
    )
    pil_images = [Image.open(image) for image in images]

    if images:
        if len(images) > 3:
            st.error("Please upload a maximum of 3 images.")
        else: 
            col = st.columns(len(images))
            
            st.subheader("Uploaded Images")
            for i,img in enumerate(pil_images):
                with col[i]:
                    st.image(img)
    #difficulty level
    selected_option=st.selectbox(
        "Select the difficulty level of the quiz",
        ("Easy", "Medium", "Hard"),
        key="difficulty_level",
        index= None
    )
    pressed= st.button("CLick the button it initiate AI",type="primary")


if pressed:
    if not images:
        st.error("You must upload at least one image to generate the note summary and quiz.")
    if not selected_option:
        st.error("You must select a difficulty level for the quiz.")
    if images and selected_option:

        #note container
        with st.container(border=True):
            st.subheader("Your Note")
            with st.spinner("Generating Note Summary..."):
                generated_note=note_generator(pil_images)
            st.markdown(generated_note)

        #audio transcription container
        with st.container(border=True):
            st.subheader("Your Audio Transcription")
            with st.spinner("Generating Audio Transcription..."):
                generated_note = generated_note.replace("#","")
                generated_note = generated_note.replace("*","")
                generated_note = generated_note.replace("-","")
                generated_note = generated_note.replace("`","")

                audio_buffer=audio_generator(generated_note)
                st.audio(audio_buffer, format="audio/mp3")

       
       
        #quiz container
        with st.container(border=True):
            st.subheader(f"Your {selected_option} Quiz")
            with st.spinner("Generating Quiz..."):
                generated_quiz=quiz_generator(pil_images,selected_option)
                st.markdown(generated_quiz)

