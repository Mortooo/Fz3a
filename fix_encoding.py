import io

path = r"home\dashboard_views.py"
with io.open(path, "r", encoding="utf-8-sig") as f:
    data = f.read()

# Reverse double-encoding that happened: original utf-8 bytes were decoded as cp1256,
# then the resulting text was saved as utf-8. Reversal: encode to cp1256, decode utf-8.
def try_reverse(s):
    b = s.encode("cp1256", errors="strict")
    return b.decode("utf-8", errors="strict")

# Try whole-file strict; fall back to per-line on failure
try:
    fixed = try_reverse(data)
    print("STRICT whole-file OK")
except Exception as e:
    print("strict failed:", type(e).__name__, e)
    lines = data.split("\n")
    fixed_lines = []
    ok = 0
    bad = 0
    for ln in lines:
        try:
            fixed_lines.append(try_reverse(ln))
            ok += 1
        except Exception:
            # leave line as-is (no arabic to fix, or unencodable char present)
            fixed_lines.append(ln)
            bad += 1
    fixed = "\n".join(fixed_lines)
    print("per-line done ok:", ok, "bad:", bad)

with io.open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(fixed)
print("WROTE FILE (utf-8, no BOM)")

# verify
with io.open(path, "r", encoding="utf-8") as f:
    check = f.read()
print("error fixed:", "بيانات الدخول غير صحيحة" in check)
print("values tab:", "قيم المبادرة" in check)
print("settings ok:", "إعدادات الموقع" in check)
print("volunteers ok:", "طلبات التطوع" in check)
