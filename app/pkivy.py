from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRaisedButton, MDTextButton, MDRoundFlatIconButton, \
    MDRectangleFlatIconButton
from kivymd.uix.button import MDFloatingActionButton
from kivy.uix.button import Button
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
import sqlite3
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

db = sqlite3.connect('app.db')
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS work (work TEXT, color TEXT)""")
db.commit()


class MainApp(MDApp):
    global cl, r, g, b, mdlayout, bv
    def build(self):
        flayout = MDFloatLayout()

        def add_button(instance):
            def line(instance):
                cursor.execute('SELECT * FROM work ')
                cursor.execute(
                    f"""UPDATE work SET work = '[s]{instance.text}[/s]' WHERE work = '{instance.text}'""")
                db.commit()

            boxlayout = MDBoxLayout(orientation='horizontal', size_hint=(1, 1), md_bg_color=(0.8, 0.85, 0.89))
            boxlayoutv = MDBoxLayout(orientation='vertical', size_hint=(0.8, 1), md_bg_color=(0.8, 0.85, 0.89))
            flayout.clear_widgets()
            boxlayout.clear_widgets()
            boxlayoutv.clear_widgets()

            cursor.execute("""SELECT work FROM work
                                    ORDER BY CASE color
                                    WHEN '[1, 0, 0, 1]' THEN 1
                                    WHEN '[1, 0.3, 0, 1.0]' THEN 2
                                    WHEN '[1, 0.78, 0, 1.0]' THEN 3
                                    WHEN '[0.19, 0.94, 0.26, 1.0]' THEN 4
                                    END;""")
            db.commit()

            e = cursor.fetchall()
            db.commit()
            cursor.execute("""SELECT color FROM work
                                    ORDER BY CASE color
                                    WHEN '[1, 0, 0, 1]' THEN 1
                                    WHEN '[1, 0.3, 0, 1.0]' THEN 2
                                    WHEN '[1, 0.78, 0, 1.0]' THEN 3
                                    WHEN '[0.19, 0.94, 0.26, 1.0]' THEN 4
                                    END;""")
            db.commit()

            col = cursor.fetchall()
            db.commit()
            for x, t in zip(col, e):
                cl = str(x)
                t = str(t)
                cl = cl.replace("'", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "")
                t = t.replace("(", "").replace(")", "").replace(",", "").replace("'", "")
                cl_list = cl.split(",")
                r = float(cl_list[0])
                g = float(cl_list[1])
                b = float(cl_list[2])

                bv = MDFlatButton(text=str(t), size_hint=(1, 1), halign="center",
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5}, theme_text_color="Custom",
                                  padding=(89, 0, 0, 0), font_size="20sp", text_color=(r, g, b), on_press=line)

                boxlayoutv.add_widget(bv)
                db.commit()
            box_button = MDBoxLayout(orientation='vertical', size_hint=(0.2, 1), md_bg_color=(0.8, 0.85, 0.89))
            color2 = [(1, 0, 0, 1), (1, 0.3, 0), (1, 0.78, 0), (0.19, 0.94, 0.26)]

            color = iter(color2)
            level = ['очень важно', 'важно', 'не важно', 'совсем не важно']
            lev = iter(level)
            for i in range(4):
                btn = MDRaisedButton(text=str(next(lev)), size_hint=(1, 1), font_size="15sp", theme_text_color="Custom",
                                     text_color="white", md_bg_color=next(color), on_press=show_dialog)
                box_button.add_widget(btn)
            boxlayout.add_widget(boxlayoutv)

            boxlayout.add_widget(box_button)
            flayout.add_widget(boxlayout)

        boxlayout = MDBoxLayout(orientation='horizontal', size_hint=(1, 1), md_bg_color=(0.8, 0.85, 0.89))

        def show_alert_dialog(instance):
            def delet(instance):
                cursor.execute('DELETE  FROM work')
                db.commit()
                dialor.dismiss()
                boxlayoutv.clear_widgets()

            dialor = MDDialog(text='Do you want to delete tasks ?',
                              buttons=[MDFlatButton(text="cancel", on_press=lambda x: dialor.dismiss()),
                                       MDFlatButton(text="ok", on_press=delet)])
            dialor.open()

        # mdlayout = MDLabel(text=str(cursor.fetchall()), size_hint=(1, 1), halign="center")
        boxlayoutv = MDBoxLayout(orientation='vertical', size_hint=(0.8, 1), md_bg_color=(0.8, 0.85, 0.89))
        bt = MDRectangleFlatIconButton(icon='application-edit-outline', font_size="48sp", icon_color='white', padding=(110, 0, 0, 0), pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(0.2, 1),
                            md_bg_color=(0.66, 0.77, 0.87), on_press=add_button)
        button_del = MDRectangleFlatIconButton(icon='delete-outline', size_hint=(0.3, 0.18), font_size="48sp", icon_color='white', padding=(110, 0, 0, 0), md_bg_color='red', on_press=show_alert_dialog)

        def show_dialog(instance):

            flayout.clear_widgets()
            boxlayout.clear_widgets()
            boxl_bt = MDBoxLayout(orientation='vertical', size_hint=(.16, 1), md_bg_color='gray')
            text_field = MDTextField(hint_text='help', pos_hint={'center_x': .8, 'center_y': .9}, size_hint=(.9, 1),
                                     multiline=True, mode='rectangle', line_color_focus=instance.md_bg_color)
            self.text_field = text_field
            line_color_focus2 = text_field.line_color_focus

            def save(instance):
                cursor.execute(f"""INSERT INTO work (work, color) VALUES(?,?)""",
                               (str(text_field.text), str(line_color_focus2)))
                db.commit()

                flayout.remove_widget(boxlayout)
                # boxlayoutv.remove_widget(mdlayout)
                start()

            button_save = MDRectangleFlatIconButton(icon='content-save-plus-outline', font_size="48sp", icon_color='white', padding=(110, 0, 0, 0), size_hint=(1, 1), md_bg_color=line_color_focus2, on_press=save)
            button_cancel = MDRectangleFlatIconButton(icon='keyboard-backspace', font_size="48sp", icon_color='white', padding=(110, 0, 0, 0), size_hint=(1, 0.55), on_press=add_button)

            boxlayout.add_widget(text_field)
            boxl_bt.add_widget(button_save)
            boxl_bt.add_widget(button_cancel)
            boxlayout.add_widget(boxl_bt)
            flayout.add_widget(boxlayout)

        def start():
            def line(instance):
                cursor.execute('SELECT * FROM work ')
                cursor.execute(
                    f"""UPDATE work SET work = '[s]{instance.text}[/s]' WHERE work = '{instance.text}'""")
                db.commit()


            flayout.clear_widgets()
            boxlayout.clear_widgets()
            boxlayoutv.clear_widgets()

            cursor.execute("""SELECT work FROM work
                        ORDER BY CASE color
                        WHEN '[1, 0, 0, 1]' THEN 1
                        WHEN '[1, 0.3, 0, 1.0]' THEN 2
                        WHEN '[1, 0.78, 0, 1.0]' THEN 3
                        WHEN '[0.19, 0.94, 0.26, 1.0]' THEN 4
                        END;""")
            db.commit()

            e = cursor.fetchall()
            db.commit()
            cursor.execute("""SELECT color FROM work
                        ORDER BY CASE color
                        WHEN '[1, 0, 0, 1]' THEN 1
                        WHEN '[1, 0.3, 0, 1.0]' THEN 2
                        WHEN '[1, 0.78, 0, 1.0]' THEN 3
                        WHEN '[0.19, 0.94, 0.26, 1.0]' THEN 4
                        END;""")
            db.commit()

            col = cursor.fetchall()
            db.commit()

            for x, t in zip(col, e):
                cl = str(x)
                t = str(t)
                cl = cl.replace("'", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "")
                t = t.replace("(", "").replace(")", "").replace(",", "").replace("'", "")
                cl_list = cl.split(",")
                r = float(cl_list[0])
                g = float(cl_list[1])
                b = float(cl_list[2])

                # mdlayout = MDLabel(text=str(t), size_hint=(1, 1), halign="center", theme_text_color="Custom", text_color=(r, g, b), padding=(285, 0, 0, 0))
                bv = MDFlatButton(text=str(t), size_hint=(1, 1), halign="center",
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5}, theme_text_color="Custom",
                                  padding=(280, 0, 0, 0), text_color=(r, g, b), font_size="20sp", on_press=line)
                cursor.execute('SELECT * FROM work ')
                db.commit()
                # box = MDBoxLayout(orientation='vertical', size_hint=(0.8, 1), md_bg_color=(0.8, 0.85, 0.89))
                # box.add_widget(bv)
                # mdlayout.add_widget(bv)

                boxlayoutv.add_widget(bv)

            boxlayout.add_widget(boxlayoutv)
            boxlayout.add_widget(button_del)

            boxlayout.add_widget(bt)
            flayout.add_widget(boxlayout)

        start()

        return flayout


MainApp().run()

