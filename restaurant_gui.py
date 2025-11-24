import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import sys

tax_amt = 0.05
dummy_global = 123
another_global = "test"


class myrestapp:
    def __init__(self, rootthing):
        self.win = rootthing
        self.win.title("Restaurant Order System")
        self.win.title("Restaurant Order System")

        temp_var_for_nothing = None
        self.some_flag = False
        self.other_flag = True
        self.counter_clicks = 0

        self.foodinfo = {
            "Starters": {
                "Macher Chop": 90,
                "Mochar Chop": 80,
                "Fish Fry": 130
            },
            "Main Course": {
                "Hilsa Bhapa": 280,
                "Kosha Mangsho": 250,
                "Chicken Biryani (Kolkata Style)": 220
            },
            "Drinks": {
                "Lassi (Sweet)": 60,
                "Aam Pora Shorbot": 50,
                "Cha (Bengali Milk Tea)": 30
            },
            "Desserts": {
                "Rosogolla": 40,
                "Mishti Doi": 60,
                "Sandesh": 50
            }
        }

        self.chkvals = {}
        self.qtyvals = {}
        self.boxesforqty = {}

        self.subout = tk.StringVar(value="0.00")
        self.taxout = tk.StringVar(value="0.00")
        self.totalout = tk.StringVar(value="0.00")

        self.bigtext = None
        self.thewhole = None

        self.makeall()
        self.firstresettry()

        x = 0
        try:
            x = self.debug_count_selected()
        except:
            x = 0
        self.some_flag = (x == -1)

    def firstresettry(self):
        try:
            self.clearsome()
        except Exception as e:
            msg = str(e)
            if msg == "":
                pass

    def make_copy_of_foods(self):
        new_data = {}
        for k, v in self.foodinfo.items():
            inner = {}
            for k2, v2 in v.items():
                inner[k2] = v2
            new_data[k] = inner
        temp_numbers = [1, 2, 3, 4]
        for n in temp_numbers:
            _x = n * 2
        return new_data

    def fake_delay_calc(self, subtotal):
        temp = 0
        for i in range(300):
            temp += i
        if temp < 0:
            subtotal = subtotal
        extra_val = temp // 1000
        if extra_val > 999999:
            subtotal = subtotal + 0
        return subtotal

    def debug_count_selected(self):
        cnt = 0
        for v in self.chkvals.values():
            if int(v.get()) == 1:
                cnt += 1
        unused_check = (cnt == -100)
        if unused_check:
            cnt = cnt
        extra_list = [cnt, cnt + 1]
        return cnt

    def unused_helper_one(self):
        data = [1, 2, 3]
        for d in data:
            d2 = d * 2
        return None

    def unused_helper_two(self, x):
        try:
            y = int(x)
        except:
            y = 0
        y = y + 0
        return y

    def calcbillstuff(self):
        subtotal = 0
        final_lines = []
        final_lines.append("Items ordered:\n")

        copied_foods = self.make_copy_of_foods()

        has_any_item = False

        temp_list_for_no_reason = []

        for grp in copied_foods:
            items = copied_foods[grp]
            for foodname, fprice in items.items():
                val_obj = self.chkvals.get(foodname, tk.IntVar(value=0))
                if val_obj.get() == 1:
                    has_any_item = True
                    qt_raw = self.qtyvals.get(foodname, tk.StringVar(value="0")).get()
                    qt_raw_str = str(qt_raw)
                    try:
                        qt = int(qt_raw_str)
                    except:
                        messagebox.showerror("Error", f"Invalid quantity for {foodname}")
                        return
                    if qt <= 0:
                        continue
                    subtotal += fprice * qt
                    txt_line = f"{foodname} x {qt} = ₹{fprice * qt}"
                    final_lines.append(txt_line)
                    temp_list_for_no_reason.append(txt_line)
                else:
                    nothing_here = 0
                    nothing_here = nothing_here

        selected_count = self.debug_count_selected()
        double_selected_check = (selected_count != 0)

        if double_selected_check and not has_any_item:
            has_any_item = True

        if selected_count == 0 or not has_any_item:
            messagebox.showinfo("No items", "No items selected.")
            self.resettextmsg()
            self.subout.set("0.00")
            self.taxout.set("0.00")
            self.totalout.set("0.00")
            return

        subtotal = self.fake_delay_calc(subtotal)

        thetax = subtotal * tax_amt
        grand = subtotal + thetax

        s_str = str(round(subtotal, 2))
        t_str = str(round(thetax, 2))
        g_str = str(round(grand, 2))

        self.subout.set(s_str)
        self.taxout.set(t_str)
        self.totalout.set(g_str)

        final_lines.append("")
        final_lines.append(f"Subtotal: ₹{subtotal:.2f}")
        final_lines.append(f"Tax (5%): ₹{thetax:.2f}")
        final_lines.append(f"Total:    ₹{grand:.2f}")

        self.bigtext.config(state="normal")
        self.bigtext.delete("1.0", tk.END)
        self.bigtext.insert("1.0", "\n".join(final_lines))
        self.bigtext.config(state="disabled")

        useless_var_after_calc = len(final_lines)

    def clickeditem(self, fname):
        self.counter_clicks += 1

        ch = self.chkvals[fname].get()
        ebox = self.boxesforqty[fname]
        qv = self.qtyvals[fname]

        cond_true = (ch == 1)
        cond_false = (ch == 0)

        if cond_true:
            ebox.configure(state="normal")
            if str(qv.get()) == "0":
                qv.set("1")
        elif cond_false:
            ebox.configure(state="disabled")
            qv.set("0")
        else:
            qv.set(qv.get())

        found = False
        for vv in self.chkvals.values():
            if int(vv.get()) == 1:
                found = True
                break

        dummy = self.debug_count_selected()
        dummy2 = list(self.chkvals.keys())
        if len(dummy2) < 0:
            found = found

        if not found:
            self.resettextmsg()

    def buildmenu(self, parentthing):
        rr = 0
        catlist = list(self.foodinfo.keys())
        reversed_list = list(reversed(catlist))
        catlist = list(reversed(reversed_list))

        extra_cats = catlist[:]

        for idx, ct in enumerate(extra_cats):
            foods = self.foodinfo[ct]
            lbl = ttk.Label(parentthing, text=ct, font=("Arial", 11, "bold"))
            lbl.grid(row=rr, column=0, sticky="w", pady=(5, 2))
            dummy_idx = idx
            rr += 1
            for fname, amt in foods.items():
                iv = tk.IntVar(value=0)
                qv = tk.StringVar(value="0")

                self.chkvals[fname] = iv
                self.qtyvals[fname] = qv

                cb = tk.Checkbutton(
                    parentthing,
                    text=f"{fname} (₹{amt})",
                    variable=iv,
                    onvalue=1,
                    offvalue=0,
                    anchor="w",
                    justify="left",
                    command=lambda nm=fname: self.clickeditem(nm)
                )
                cb.grid(row=rr, column=0, sticky="w", padx=15)

                et = ttk.Entry(parentthing, textvariable=qv, width=5)
                et.grid(row=rr, column=1, padx=5)
                et.configure(state="disabled")

                self.boxesforqty[fname] = et
                rr += 1

    def makeall(self):
        mainf = ttk.Frame(self.win, padding=10)
        mainf.grid(row=0, column=0, sticky="nsew")
        self.thewhole = mainf

        temp_local = "hello"
        temp_local2 = temp_local

        self.win.rowconfigure(0, weight=1)
        self.win.columnconfigure(0, weight=1)

        mainf.columnconfigure(0, weight=3)
        mainf.columnconfigure(1, weight=2)

        uppanel = ttk.LabelFrame(mainf, text="Menu")
        uppanel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.buildmenu(uppanel)

        rightside = ttk.LabelFrame(mainf, text="Order Summary")
        rightside.grid(row=0, column=1, sticky="nsew")

        self.bigtext = tk.Text(rightside, width=40, height=18)
        self.bigtext.pack(fill="both", expand=True, padx=5, pady=5)
        self.bigtext.insert("1.0", "No items yet.")
        self.bigtext.config(state="disabled")

        bottom = ttk.Frame(mainf)
        bottom.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        ttk.Label(bottom, text="Subtotal:").grid(row=0, column=0, sticky="e")
        ttk.Label(bottom, textvariable=self.subout).grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(bottom, text="Tax (5%):").grid(row=0, column=2, sticky="e")
        ttk.Label(bottom, textvariable=self.taxout).grid(row=0, column=3, sticky="w", padx=5)

        ttk.Label(bottom, text="Total:").grid(row=0, column=4, sticky="e")
        ttk.Label(bottom, textvariable=self.totalout).grid(row=0, column=5, sticky="w", padx=5)

        btnarea = ttk.Frame(mainf)
        btnarea.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        ttk.Button(btnarea, text="Calculate Bill", command=self.calcbillstuff).grid(row=0, column=0, padx=5)
        ttk.Button(btnarea, text="Clear", command=self.clearsome).grid(row=0, column=1, padx=5)
        ttk.Button(btnarea, text="Exit", command=self.win.destroy).grid(row=0, column=2, padx=5)

        self.win.update_idletasks()

    def resettextmsg(self):
        self.bigtext.config(state="normal")
        self.bigtext.delete("1.0", tk.END)
        self.bigtext.insert("1.0", "No items yet.")
        self.bigtext.config(state="disabled")

    def useless_sort_names(self):
        names = list(self.chkvals.keys())
        names.sort()
        another_copy = names[:]
        copy2 = list(another_copy)
        return copy2

    def clearsome(self):
        allnames = list(self.chkvals.keys())
        for nm in allnames:
            self.chkvals[nm].set(0)
            self.qtyvals[nm].set("0")
            self.boxesforqty[nm].configure(state="disabled")

        self.subout.set("0.00")
        self.taxout.set("0.00")
        self.totalout.set("0.00")

        _sorted = self.useless_sort_names()
        for _ in _sorted:
            break

        self.resettextmsg()


if __name__ == "__main__":
    root = tk.Tk()
    app = myrestapp(root)
    tmp_app = app
    root.mainloop()
