from typing import Union
import cv2
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import bisect as bs

device = 'cuda' if torch.cuda.is_available() else 'cpu'

mtcnn_model = MTCNN(keep_all = True, device = device)
resnet_model = InceptionResnetV1(pretrained = 'vggface2').eval().to(device)


def get_faces(img: Union[str, list[str]]) -> list[list]:
    '''
    This function is used to get the faces from the image(s).
    '''

    if isinstance(img, str):
        img = [img]

    found_faces = []
    telly = []

    for im in img:
        im = cv2.imread(im)
        img_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        faces = mtcnn_model(img_rgb, return_prob = False)
        if faces is None:
            continue
        s = len(found_faces)
        found_faces.extend(list(faces))
        telly.append(s)

    return found_faces, telly


def search_faces(
        template: list[str], search_images: list[str], batch_size: int = 100, threshold: float = 0.8
    ) -> set[int]:
    '''
    This function is used to match the faces in the search images with the template.
    Applies batch operation of `batch_size` images per iteration.
    '''

    template = get_faces(template)[0]

    template = torch.stack(template).to(device)
    face_embeddings_template = resnet_model(template).detach().cpu().numpy()
    matched_images = []

    for i in range(0, len(search_images), batch_size):
        images = search_images[i:i + batch_size]
        faces, telly = get_faces(images)

        faces_attached = torch.stack(faces).to(device)
        face_embeddings_search = resnet_model(faces_attached).detach().cpu().numpy()

        for j in range(len(face_embeddings_search)):
            for k in range(len(face_embeddings_template)):
                if np.linalg.norm(face_embeddings_search[j] - face_embeddings_template[k]) < threshold:
                    print(telly, j, bs.bisect_left(telly, j))
                    matched_image_idx = i + bs.bisect_left(telly, j)
                    print("matched", search_images[matched_image_idx])
                    matched_images.append(search_images[matched_image_idx])
                    break

    return matched_images