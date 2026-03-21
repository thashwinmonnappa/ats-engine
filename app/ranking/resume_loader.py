import os

class ResumeLoader:

    def load_resumes(self, folder_path):

        resumes = []

        for file in os.listdir(folder_path):

            if file.endswith(".pdf") or file.endswith(".docx"):

                resumes.append(os.path.join(folder_path, file))

        return resumes