#!/usr/bin/env python3
"""CLI for searching and exporting the HTTP status-code dataset."""
from __future__ import annotations
import argparse, csv, json, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; CODES_PATH=ROOT/"codes.json"; I18N_DIR=ROOT/"i18n"

def load_codes() -> list[dict]:
    try: data=json.loads(CODES_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError: print(f"Error: {CODES_PATH} not found.",file=sys.stderr); raise SystemExit(1)
    if not isinstance(data,list): print("Error: codes.json must contain a JSON array.",file=sys.stderr); raise SystemExit(1)
    return data

def get_supported_langs() -> list[str]:
    if not I18N_DIR.exists(): return []
    return sorted(path.stem for path in I18N_DIR.glob("*.json") if path.name!="manifest.json")

def load_translations(lang: str, strict: bool=True) -> dict:
    path=I18N_DIR/f"{lang}.json"
    if not path.exists():
        if strict: raise ValueError(f"Unsupported language '{lang}'. Available: {', '.join(get_supported_langs())}")
        return {}
    data=json.loads(path.read_text(encoding="utf-8")); return data if isinstance(data,dict) else {}

def translation_for(item:dict,translations:dict)->dict:
    if item["id"] in translations: return translations[item["id"]]
    if item["type"]=="standard": return translations.get(str(item["code"]),{})
    return {}

def localized_item(item:dict,translations:dict)->dict:
    result=dict(item); tr=translation_for(item,translations); result["phrase"]=tr.get("phrase",item["phrase"]); result["description"]=tr.get("description",item["description"]); return result

def matches_query(item:dict,query:str,translations:dict)->bool:
    q=query.casefold(); loc=localized_item(item,translations)
    haystack=" ".join(str(v) for v in (item["id"],item["code"],item.get("provider",""),item.get("type",""),item.get("status",""),item.get("class",""),loc.get("phrase",""),loc.get("description",""),item.get("reference",""))).casefold()
    return q in haystack

def filter_items(items:list[dict],query:str,translations:dict,item_type:str|None=None,provider:str|None=None,status:str|None=None)->list[dict]:
    query=query.strip(); class_filter=len(query)==3 and query.endswith("xx") and query[0].isdigit(); result=[]
    for item in items:
        if item_type and item["type"]!=item_type: continue
        if provider and item.get("provider")!=provider: continue
        if status and item.get("status")!=status: continue
        if query.lower()=="all": matched=True
        elif class_filter: matched=item["class"].startswith(query.lower())
        elif query.isdigit(): matched=item["code"]==int(query)
        else: matched=matches_query(item,query,translations)
        if matched: result.append(localized_item(item,translations))
    return result

def format_result(item:dict,use_color:bool=True)->str:
    green="\033[1;32m" if use_color else ""; cyan="\033[1;36m" if use_color else ""; blue="\033[4;34m" if use_color else ""; reset="\033[0m" if use_color else ""
    lines=[f"{green}HTTP {item['code']}{reset}: {cyan}{item['phrase']}{reset}",f"ID: {item['id']}",f"Type: {item['type']} | Provider: {item.get('provider','-')}",f"Class: {item['class']} | Status: {item['status']}",f"Description: {item['description']}"]
    if item.get("reference"): lines.append(f"Reference: {item['reference']}")
    source=item.get("source") or {}
    if source.get("url"): lines.append(f"Source: {blue}{source['url']}{reset}")
    if item.get("mdn_link"): lines.append(f"MDN: {blue}{item['mdn_link']}{reset}")
    lines.append("-"*56); return "\n".join(lines)

def export_results(results:list[dict],output_format:str,output_file:Path)->None:
    if output_format=="json": output_file.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); return
    if output_format=="csv":
        fields=["id","code","type","provider","phrase","class","status","description","reference","source_url","verified_at"]
        with output_file.open("w",newline="",encoding="utf-8") as handle:
            writer=csv.DictWriter(handle,fieldnames=fields); writer.writeheader()
            for item in results:
                source=item.get("source") or {}; writer.writerow({"id":item["id"],"code":item["code"],"type":item["type"],"provider":item.get("provider",""),"phrase":item["phrase"],"class":item["class"],"status":item["status"],"description":item["description"],"reference":item.get("reference",""),"source_url":source.get("url",""),"verified_at":item.get("verified_at") or ""})
        return
    if output_format=="md":
        def esc(value:object)->str: return str(value).replace("|","\\|").replace("\n"," ")
        with output_file.open("w",encoding="utf-8") as handle:
            handle.write("# HTTP Status Codes Export\n\n| Code | ID | Phrase | Type | Provider | Status | Description |\n|---:|---|---|---|---|---|---|\n")
            for item in results: handle.write(f"| {item['code']} | {esc(item['id'])} | {esc(item['phrase'])} | {esc(item['type'])} | {esc(item.get('provider',''))} | {esc(item['status'])} | {esc(item['description'])} |\n")
        return
    raise ValueError(f"Unsupported export format: {output_format}")

def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description="Search standard and vendor-specific HTTP status codes."); parser.add_argument("query",nargs="?"); parser.add_argument("--lang",default="en"); parser.add_argument("--list-langs",action="store_true"); parser.add_argument("--type",choices=["standard","vendor"],dest="item_type"); parser.add_argument("--provider"); parser.add_argument("--status",choices=["active","temporary","unused","obsoleted"]); parser.add_argument("--export",choices=["json","csv","md"],dest="export_format"); parser.add_argument("--out",type=Path); parser.add_argument("--no-color",action="store_true"); args=parser.parse_args(argv)
    if args.list_langs:
        for lang in get_supported_langs(): print(lang)
        return 0
    if not args.query: parser.print_help(); return 1
    try: translations=load_translations(args.lang,strict=True)
    except (ValueError,json.JSONDecodeError) as exc: print(f"Error: {exc}",file=sys.stderr); return 2
    results=filter_items(load_codes(),args.query,translations,item_type=args.item_type,provider=args.provider,status=args.status)
    if not results: print(f"No results found for '{args.query}'."); return 3
    if args.export_format:
        output=args.out or Path(f"export_{args.query}.{args.export_format}"); export_results(results,args.export_format,output); print(f"Exported {len(results)} result(s) to {output}"); return 0
    use_color=not args.no_color and sys.stdout.isatty() and os.getenv("NO_COLOR") is None
    for item in results: print(format_result(item,use_color=use_color))
    return 0
if __name__=="__main__": raise SystemExit(main())
