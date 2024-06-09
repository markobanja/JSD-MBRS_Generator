from gui import GUI

def launch():
    try:
        gui = GUI()
        gui.run()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    launch()
