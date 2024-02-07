import os


def save_uploaded_file(uploaded_file):
    file_path = os.path.join("images", uploaded_file.name)
    if os.path.exists(file_path):
        pass
    else:
        with open(os.path.join("images", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    return uploaded_file.name
