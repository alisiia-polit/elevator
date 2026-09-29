from tkinter import *
import time

MAX_WEIGHT = 630
MAX_FLOOR = 10
is_emergency = False

def emergency():
    global is_emergency
    if is_emergency:
        emergency_btn["bg"] = "#66ff66"
    else:
        emergency_btn["bg"] = "#ff8080"
    is_emergency = not is_emergency

def move():
    global weight_field, current_floor_field, preferred_floor_field, result_field, root
    result_field.delete(1.0, END)

    if is_emergency:
        result_field.insert(END, "натиснуто кнопку аварійного виклику\n")
        result_field.insert(END, "аварійне зупинення руху\n")
        return

    params = (weight_field.get(), current_floor_field.get(), preferred_floor_field.get())
    if "" in params:
        result_field.insert(END, "усі поля повинні бути заповнені!")
        return



    try:
        weight = float(weight_field.get())
        current_floor = int(current_floor_field.get())
        preferred_floor = int(preferred_floor_field.get())
    except ValueError:
        result_field.insert(END, "значення повинні бути числовими!")
        return


    if any(p <= 0 for p in (weight, current_floor, preferred_floor)):
        result_field.insert(END, "значення повинні бути додатніми!")
        return

    if any(f > MAX_FLOOR for f in (current_floor, preferred_floor)):
        result_field.insert(END, f"будівля має {MAX_FLOOR} поверхів!")
        return

    match door_state.get():
        case "open":
            result_field.insert(END,"двері відчинені")
            return
        case "barrier":
            result_field.insert(END,"увага! перешкода у дверях")
            return
        case "close":
            result_field.insert(END,"двері зачинені\n")

    if weight > MAX_WEIGHT:
        result_field.insert(END, "перенавантаження! зменшіть вагу")
        return

    result_field.insert(END, "вага в нормі\n")

    if current_floor == preferred_floor:
        result_field.insert(END,"ви вже на потрібному поверсі")
        return
    elif preferred_floor > current_floor:
        result_field.insert(END, "напрямок руху: вгору\n")
    else:
        result_field.insert(END,"напрямок руху: вниз\n")

    result_field.insert(END, "поїздка розпочинається\n")

    move_time = abs(current_floor - preferred_floor) * 1000

    root.after(
        move_time,
        lambda: result_field.insert(
            END, f"ліфт прибув на {preferred_floor} поверх\nїхали {move_time} мс"
        )
    )

root = Tk()
root.title("система керування ліфтом")
root.geometry("700x600")

emergency_btn = Button(root,
                       text="кнопка аварійного виклику",
                       bg="#66ff66",
                       fg="black",
                       command=emergency)


move_btn = Button(root,
                  text="кнопка руху",
                  command=move)
emergency_btn.pack(pady=10)
move_btn.pack(pady=10)

door_state = StringVar()
door_state.set("close")
btn_open = Radiobutton(root, text="двері відчинено", variable=door_state, value="open")
btn_close = Radiobutton(root, text="двері зачинено", variable=door_state, value="close")
btn_barrier = Radiobutton(root, text="є перешкода", variable=door_state, value="barrier")

btn_open.pack(side="top", pady=10)
btn_close.pack(side="top", pady=10)
btn_barrier.pack(side="top", pady=10)

Label1 = Label(text="введіть сумарну вагу людей в кабіні(кг):")
weight_field = Entry(root, width=18, bd=5)
Label2 = Label(text="введіть поточний поверх(1-10): ")
current_floor_field = Entry(root, width=18, bd=5)
Label3 = Label(text="введіть потрібний поверх(1-10): ")
preferred_floor_field = Entry(root, width=18, bd=5)

Label1.pack()
weight_field.pack(pady=10)
Label2.pack()
current_floor_field.pack(pady=10)
Label3.pack()
preferred_floor_field.pack(pady=10)


# doors_field = Label(font="Arial 20").pack
# direction_field = Label(font="Arial 20").pack
result_field = Text(root, font="20")
result_field.pack()
# result_field2 = Label(font="Arial 20").pack



root.mainloop()