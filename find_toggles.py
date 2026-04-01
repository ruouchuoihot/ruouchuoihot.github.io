import os, glob, json

log_dir = r"C:\Users\Duong\.gemini\antigravity\brain\fc93f8fd-59ee-472b-be2c-2deb4414758e\.system_generated\steps"
files = glob.glob(os.path.join(log_dir, "*", "output.txt"))

for f in files:
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        start = content.find('{')
        if start == -1: continue
        js = json.loads(content[start:])
        
        if 'results' in js:
            for b in js['results']:
                if b.get('has_children') == True:
                    b_id = b.get('id')
                    b_type = b.get('type')
                    name = ''
                    if b_type and b_type in b:
                        rt = b[b_type].get('rich_text', [])
                        if rt:
                            name = "".join([x.get('plain_text', '') for x in rt])
                    # Print without accents carefully
                    print(f"{b_id} | {name.encode('ascii', 'ignore').decode()}")
    except:
        pass
