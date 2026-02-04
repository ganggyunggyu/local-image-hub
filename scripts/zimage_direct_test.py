"""Z-Image 직접 로드 테스트 - CPU offload + float32"""

import sys
import torch
import time

print("Z-Image 직접 로드 테스트 (CPU offload)", flush=True)
print(f"Device: MPS available = {torch.backends.mps.is_available()}", flush=True)

print("1. ZImagePipeline import...", flush=True)
try:
    from diffusers import ZImagePipeline
    print("   OK", flush=True)
except ImportError as e:
    print(f"   FAIL: {e}", flush=True)
    sys.exit(1)

print("2. 모델 로딩 (float32, CPU offload)...", flush=True)
t0 = time.time()
try:
    pipe = ZImagePipeline.from_pretrained(
        "Tongyi-MAI/Z-Image",
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    print(f"   로드 완료: {time.time() - t0:.1f}s", flush=True)
except Exception as e:
    print(f"   FAIL: {e}", flush=True)
    sys.exit(1)

print("3. CPU offload 활성화 (MPS)...", flush=True)
t1 = time.time()
try:
    pipe.enable_model_cpu_offload(device="mps")
    print(f"   완료: {time.time() - t1:.1f}s", flush=True)
except Exception as e:
    print(f"   enable_model_cpu_offload FAIL: {e}", flush=True)
    print("   대신 sequential_cpu_offload 시도...", flush=True)
    try:
        pipe.enable_sequential_cpu_offload(device="mps")
        print(f"   sequential 완료: {time.time() - t1:.1f}s", flush=True)
    except Exception as e2:
        print(f"   sequential도 FAIL: {e2}", flush=True)
        print("   수동 MPS 이동 시도...", flush=True)
        pipe.to("mps")
        print(f"   수동 이동 완료: {time.time() - t1:.1f}s", flush=True)

print("4. 이미지 생성 (50 steps, cfg=4.0)...", flush=True)
t2 = time.time()
try:
    generator = torch.Generator(device="cpu").manual_seed(42)
    result = pipe(
        prompt="japanese spitz puppy, fluffy white fur, photorealistic",
        negative_prompt="ugly, blurry, deformed",
        height=1024,
        width=1024,
        num_inference_steps=50,
        guidance_scale=4.0,
        cfg_normalization=False,
        generator=generator,
    )
    image = result.images[0]
    out_path = "outputs/20260202_zimage_full/direct_test_spitz.webp"
    from pathlib import Path
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path, format="WEBP", quality=90)
    fsize = Path(out_path).stat().st_size
    print(f"   생성 완료: {time.time() - t2:.1f}s", flush=True)
    print(f"   저장: {out_path} ({fsize:,} bytes)", flush=True)
except Exception as e:
    print(f"   FAIL: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print(f"\n총 소요: {time.time() - t0:.1f}s", flush=True)
