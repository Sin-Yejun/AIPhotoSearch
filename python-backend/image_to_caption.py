import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import os

# CLIP 모델과 프로세서 로드
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# 이미지 폴더에 있는 모든 이미지를 로드하고 전처리
def load_images_from_folder(folder_path):
    images = []
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img_path = os.path.join(folder_path, filename)
            try:
                image = Image.open(img_path).convert("RGB")  # 이미지를 RGB로 변환하여 CLIP 모델 호환성 유지
                images.append(image)
                image_paths.append(img_path)
            except Exception as e:
                print(f"이미지를 로드하는 데 실패했습니다: {img_path}, 에러: {e}")
    return images, image_paths

# 이미지와 텍스트(검색어) 간 유사도 계산
def calculate_similarity(images, search_text):
    inputs = processor(text=[search_text], images=images, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # 이미지와 텍스트 간의 유사성 점수
    logits_per_image = outputs.logits_per_image  # (batch_size, 1) 형태
    probs = logits_per_image.softmax(dim=0)  # 소프트맥스 적용하여 확률 계산
    return probs

# 모든 이미지와 그 확률을 출력
def print_all_image_probabilities(image_paths, probs):
    print("모든 이미지의 확률:")
    for i, prob in enumerate(probs):
        print(f"이미지 이름: {os.path.basename(image_paths[i])}, 확률: {prob.item() * 100:.2f}%")

# 이미지 폴더 경로와 검색어 설정
folder_path = 'images'  # 이미지가 저장된 폴더 경로
search_text = "sea"  # 사용자가 입력하는 검색어 (예: 바닷가)

# 이미지 로드
images, image_paths = load_images_from_folder(folder_path)

# 만약 폴더에 이미지가 없다면 종료
if not images:
    print("폴더에서 이미지를 찾을 수 없습니다.")
else:
    # 유사도 계산
    probs = calculate_similarity(images, search_text)

    # 모든 이미지의 확률 출력
    print_all_image_probabilities(image_paths, probs)
