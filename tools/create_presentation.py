from pathlib import Path
import subprocess
import imageio_ffmpeg

root = Path(__file__).resolve().parents[1]
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
output_dir = root / "output"
output_dir.mkdir(exist_ok=True)
intro = output_dir / "hme-intro.mp4"
body = output_dir / "hme-body.mp4"
concat = output_dir / "hme-concat.txt"
final = output_dir / "HME-Motors-apresentacao.mp4"
cover = root / "public" / "image.png"
recording = Path(r"C:\Projetos\HME motors\Gravando 2026-08-13 133756.mp4")
music = Path(r"C:\Users\mvran\Downloads\alexzavesa-dance-playful-night-510786.mp3")

def run(args):
    subprocess.run([ffmpeg, "-y", *map(str, args)], check=True)

run([
    "-loop", "1", "-i", cover, "-t", "3", "-vf",
    "scale=1356:646:force_original_aspect_ratio=increase,crop=1356:646,drawbox=x=0:y=0:w=iw:h=ih:color=black@0.3:t=fill",
    "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", intro,
])
run([
    "-i", recording, "-t", "52", "-vf", "scale=1356:646:force_original_aspect_ratio=decrease,pad=1356:646:(ow-iw)/2:(oh-ih)/2:color=black",
    "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", body,
])
concat.write_text(f"file '{intro.as_posix()}'\nfile '{body.as_posix()}'\n", encoding="utf-8")
run([
    "-f", "concat", "-safe", "0", "-i", concat,
    "-stream_loop", "-1", "-i", music,
    "-filter_complex", "[1:a]volume=0.38,afade=t=in:st=0:d=1,afade=t=out:st=51:d=3[a]",
    "-map", "0:v:0", "-map", "[a]", "-t", "55", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final,
])
print(final)
