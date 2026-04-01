import json
import os
import urllib.request
from pathlib import Path

# Mapping of file contexts to their actual Date and Title
pages_to_patch = [
    {
        "file_md": "2026-04-01-building-dfir-home-lab.md",
        "img_dir": "dfir",
        "toggles": [
            r"C:\Users\Duong\.gemini\antigravity\brain\fc93f8fd-59ee-472b-be2c-2deb4414758e\.system_generated\steps\386\output.txt",
            r"C:\Users\Duong\.gemini\antigravity\brain\fc93f8fd-59ee-472b-be2c-2deb4414758e\.system_generated\steps\387\output.txt"
        ]
    },
    {
        "file_md": "2026-04-01-using-splunk-es.md",
        "img_dir": "splunk",
        "toggles": [
            r"C:\Users\Duong\.gemini\antigravity\brain\fc93f8fd-59ee-472b-be2c-2deb4414758e\.system_generated\steps\388\output.txt",
            r"C:\Users\Duong\.gemini\antigravity\brain\fc93f8fd-59ee-472b-be2c-2deb4414758e\.system_generated\steps\389\output.txt"
        ]
    },
    {
        "file_md": "2026-04-01-splunk-soar.md",
        "img_dir": "splunk",
        "toggles": [
            r"C:\Users\Duong\.gemini\antigravity\brain\fc93f8fd-59ee-472b-be2c-2deb4414758e\.system_generated\steps\390\output.txt",
            """{"results": []}""" # 391 had no children essentially
        ]
    }
]

blog_dir = r"e:\app\ctf-blog"
posts_dir = os.path.join(blog_dir, "_posts")

def parse_rich_text(rt_array):
    out = ""
    for rt in rt_array:
        text = rt.get("plain_text", "")
        if not text and rt.get("text"):
            text = rt["text"].get("content", "")
        
        ann = rt.get("annotations", {})
        if ann.get("code"):
            text = f"`{text}`"
        elif ann.get("bold"):
            text = f"**{text}**"
        elif ann.get("italic"):
            text = f"*{text}*"
        
        if rt.get("href"):
            text = f"[{text}]({rt['href']})"
        out += text
    return out

for data in pages_to_patch:
    post_path = os.path.join(posts_dir, data["file_md"])
    if not os.path.exists(post_path): continue
        
    target_img_dir = os.path.join(blog_dir, "assets", "images", data["img_dir"])
    img_rel_path = f"/assets/images/{data['img_dir']}/"
    os.makedirs(target_img_dir, exist_ok=True)
    
    with open(post_path, "r", encoding="utf-8") as f:
        existing_md = f.read()

    # We will just append the new markdown to the end for simplicity,
    # OR replace the toggle headings with their expanded content.
    # Since existing_md already has "## Getting started with DFIR", we can string-replace or just append.
    # Appending is safer, we'll try to find the heading and insert.
    for t_idx, t_path in enumerate(data["toggles"]):
        if not os.path.exists(t_path) and not t_path.startswith("{"): continue
        
        if t_path.startswith("{"):
            json_str = t_path
        else:
            with open(t_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                json_str = ""
                for line in lines:
                    if line.startswith("1: "): json_str = line[3:]; break
                    elif line.startswith("{"): json_str = line; break
                if not json_str: json_str = "".join(lines)
        
        try:
            content_json = json.loads(json_str)
        except Exception as e:
            continue
            
        markdown = ""
        for block in content_json.get("results", []):
            btype = block.get("type", "")
            bdata = block.get(btype, {})
            
            if btype == "paragraph":
                text = parse_rich_text(bdata.get("rich_text", []))
                if text: markdown += f"{text}\\n\\n"
            elif btype == "bulleted_list_item":
                text = parse_rich_text(bdata.get("rich_text", []))
                markdown += f"- {text}\\n"
            elif btype == "numbered_list_item":
                text = parse_rich_text(bdata.get("rich_text", []))
                markdown += f"1. {text}\\n"
            elif btype == "code":
                lang = bdata.get("language", "")
                code_text = parse_rich_text(bdata.get("rich_text", []))
                markdown += f"```{lang}\\n{code_text}\\n```\\n\\n"
            elif btype == "image":
                file_obj = bdata.get("file", {})
                img_url = file_obj.get("url", "")
                if img_url:
                    img_name = f"{block.get('id', 'img')}.png"
                    img_path = os.path.join(target_img_dir, img_name)
                    try:
                        urllib.request.urlretrieve(img_url, img_path)
                        markdown += f"![image]({img_rel_path}{img_name})\\n\\n"
                    except Exception as e:
                        print(f"Failed to dl image {img_url}")
            elif btype == "divider":
                markdown += "---\\n\\n"

        markdown = markdown.replace("\\n", "\n")
        # Find the Nth heading in the file that was generated for the toggle and insert after it
        # Actually, let's just append carefully or recreate. 
        # A simple append for now:
        if markdown.strip():
            existing_md += "\n\n" + markdown

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(existing_md)
        
print("Patching complete")
