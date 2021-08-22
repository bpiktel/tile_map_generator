from tkinter import (
    Frame, Canvas, Scrollbar, Label, Tk, Button, Toplevel, Entry, colorchooser,
    messagebox, Menu, filedialog)
import tkinter as tk

from PIL import ImageTk

from src.tile_map_io import TileMapIO
from src.visualisation import TileMapVisualisation
from src.tile_map import TileMap
from src.generator import TileMapGenerator
from src.tile import Tile, TileTreeNode


class MapViewer(Frame):
    """
    Window in which tile image is displayed
    """

    def __init__(self, root, map_image):
        Frame.__init__(self, root)
        root.title("Map Viewer")
        self.pack(fill=tk.BOTH)

        top_menu = Menu(root)
        file_menu = Menu(top_menu, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_image)
        top_menu.add_cascade(label="File", menu=file_menu)
        root.config(menu=top_menu)

        self.map_image = map_image
        img_width, img_height = map_image.size

        canv = Canvas(self)
        canv.config(width=img_width, height=img_height)

        scrollbar_v = Scrollbar(self, orient=tk.VERTICAL)
        scrollbar_h = Scrollbar(self, orient=tk.HORIZONTAL)
        scrollbar_v.config(command=canv.yview)
        scrollbar_h.config(command=canv.xview)
        canv.config(yscrollcommand=scrollbar_v.set)
        canv.config(xscrollcommand=scrollbar_h.set)

        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)

        canv.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        canv.config(scrollregion=(0, 0, img_width, img_height))

        self.image = ImageTk.PhotoImage(map_image)
        self.img = canv.create_image(0, 0, anchor="nw", image=self.image)

        self.update()

        width_max = img_width+scrollbar_h.winfo_height()+4
        height_max = img_height+scrollbar_v.winfo_width()+4
        root.maxsize(width=width_max, height=height_max)

    def save_image(self):
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save map",
                filetypes=(("PNG", "*.png"), ("All files", "*.*")))
            TileMapIO.save_map_image(self.map_image, file_path)
        except Exception as e:
            messagebox.showerror("Coulnd't save image", str(e))


class GenerationGUI(Frame):
    """
    Main window of application
    """

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root

        root.title("Tile Map Generator")

        top_menu = Menu(root)
        file_menu = Menu(top_menu, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_map)
        file_menu.add_command(label="Open", command=self.load_map)
        top_menu.add_cascade(label="File", menu=file_menu)
        root.config(menu=top_menu)

        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 2, weight=1)
        self.pack(fill=tk.BOTH)

        self.tile_info_container = Frame(self)
        self.tiles_info_list = self.get_default_tiles_info()
        self.update_tiles_info()
        self.tile_info_container.grid(
            row=0, column=0, columnspan=3, padx=10, pady=10)

        self.map_size_frame = Frame(self)
        self.map_size_label = Label(self.map_size_frame, text="Map size:")
        self.map_size_label.grid(row=0, column=0)
        self.x_map_size = Entry(self.map_size_frame, width=7)
        self.x_map_size.grid(row=0, column=1)
        self.map_size_x_label = Label(self.map_size_frame, text="x")
        self.map_size_x_label.grid(row=0, column=2)
        self.y_map_size = Entry(self.map_size_frame, width=7)
        self.y_map_size.grid(row=0, column=3)
        self.map_size_frame.grid(row=3, column=0, columnspan=3)

        self.generate_button = Button(
            self, text="Generate", command=self.generate_map)
        self.generate_button.grid(row=4, column=0, padx=10, pady=10)
        self.update_tiles_button = Button(
            self, text="Update tiles", command=self.change_tiles_on_map)
        self.update_tiles_button.grid(row=4, column=1, padx=10, pady=10)
        self.view_map_button = Button(
            self, text="View map", command=self.view_map)
        self.view_map_button.grid(row=4, column=2, padx=10, pady=10)

        # initializing map with sample tiles
        self.tiles = self.construct_ttn(self.tiles_info_list[0])
        self.map_ = TileMap(10, 10, self.tiles)

    def view_map(self):
        if self.map_ is not None:
            self._map_window = Toplevel(self.root)
            image = TileMapVisualisation.get_map_image(self.map_)
            MapViewer(self._map_window, image).pack(
                side="top", fill="both", expand=True)

    def change_tiles_on_map(self):
        try:
            self.update_tiles()
            self.view_map()
        except Exception as e:
            messagebox.showerror("Cannot generate map", str(e))

    def update_tiles(self):
        for tile in self.tiles_info_list:
            if tile.edit_mode:
                raise TileInEditModeError("All tiles must be saved")

        self.tiles = self.construct_ttn(self.tiles_info_list[0])
        self.map_.update_tiles(self.tiles)

    def generate_map(self):
        try:
            size_x = self.x_map_size.get()
            size_y = self.y_map_size.get()
            if len(size_x) == 0 or len(size_y) == 0:
                raise EmptyEntryFieldError("Map size must be specified")
            if not size_x.isdigit() or not size_y.isdigit():
                raise TypeError("Map size must be positive integer")
            size_x = int(size_x)
            size_y = int(size_y)
            self.update_tiles()
            self.map_ = TileMap(size_y, size_x, self.tiles)
            self.map_ = TileMapGenerator().generate_map(self.map_)
            self.view_map()
        except Exception as e:
            messagebox.showerror("Cannot generate map", str(e))

    def get_default_tiles_info(self):
        """Returns sample data"""
        return [RootTileInfoSegment(self.tile_info_container, self),
                TileInfoSegment(self.tile_info_container, self, 0, 1,
                                name="grass", color="green", level=1)]

    def update_tiles_info(self):
        """Updates tiles info displayed in main window"""
        for row, block in enumerate(self.tiles_info_list):
            block.grid(row=row, sticky="W")

    def insert_new_tile(self, new_tile, parent_tile_id):
        for i, tile in enumerate(self.tiles_info_list):
            if tile.tile_id == parent_tile_id:
                self.tiles_info_list.insert(i+1, new_tile)
                return

    def remove_tile_from_list(self, tile_info):
        self.tiles_info_list.remove(tile_info)

    def save_map(self):
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save map",
                filetypes=(("Pickle files", "*.pickle"), ("All files", "*.*")))
            TileMapIO.save_map_to_file(self.map_, file_path)
        except Exception as e:
            messagebox.showerror("Couldn;t save map", str(e))

    def load_map(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Load map",
                filetypes=(("Pickle files", "*.pickle"), ("All files", "*.*")))
            load = TileMapIO.load_map_from_file(file_path)
            if load is None:
                return
            self.map_ = load
            self.tiles = self.map_.get_tiles()
            self.load_tiles_info_from_tiles()
            self.update_tiles_info()
        except Exception as e:
            messagebox.showerror("Couldn't load map", str(e))

    def construct_ttn(self, first_tile):
        """Constructs TileTreeNode from parsed tiles data"""
        ttn = TileTreeNode(first_tile.construct_tile_object())
        for tile in self.tiles_info_list:
            if tile.parent_tile_id == first_tile.tile_id:
                child_ttn = self.construct_ttn(tile)
                ttn.add_child(child_ttn)
        return ttn

    def load_tiles_info_from_tiles(self):
        """Creates new tiles info list from loaded tiles data"""
        new_tiles_info = []
        root_tile = self.tiles.get_tile()
        new_tiles_info.append(RootTileInfoSegment(
            self.tile_info_container, self,
            root_tile.get_name(), root_tile.get_color()))
        new_tiles_info += self.load_ttn(self.tiles, root_tile.get_id(), 1)
        self.tiles_info_list = new_tiles_info

    def load_ttn(self, ttn, parent_id, level=1):
        """Loads tiles info from TileTreeNode, creates tile hierarchy"""
        tiles_info = []
        for child_ttn in ttn.get_children():
            tile = child_ttn.get_tile()
            tiles_info.append(
                self.get_tile_info_segment(tile, self, parent_id, level))
            tiles_info += self.load_ttn(child_ttn, tile.get_id(), level+1)
        return tiles_info

    def get_tile_info_segment(self, tile, root, parent_id, level):
        """Returns tile info segment representing data in Tile object"""
        return TileInfoSegment(
            self.tile_info_container, self, parent_id, tile_id=tile.get_id(),
            name=tile.get_name(), color=tile.get_color(), fill=tile.get_fill(),
            islands=tile.get_islands(), level=level)


class TileInfoSegment(Frame):
    """
    Widget containing single tile data and options to edit it
    """

    def __init__(self, root, main_gui, parent_tile_id, tile_id=0, name="name",
                 color="#000000", fill=0.5, islands=1, level=0):
        Frame.__init__(self, root)
        self.main_gui = main_gui
        self.tile_id = tile_id
        self.parent_tile_id = parent_tile_id
        self.tile_name = name
        self.tile_color = color
        self.tile_fill = fill
        self.tile_islands = islands

        self.indent_label = Label(self, text=level*"\t")
        self.indent_label.grid(row=0, column=0)
        self.id_label = Label(self, text="ID:")
        self.id_label.grid(row=0, column=1)
        id_text = tk.StringVar()
        id_text.set(self.tile_id)
        self.id_entry = Entry(self, width=2, textvariable=id_text)
        self.id_entry.grid(row=0, column=2)
        self.name_label = Label(self, text="name:")
        self.name_label.grid(row=0, column=3)
        name_text = tk.StringVar()
        name_text.set(self.tile_name)
        self.name_entry = Entry(self, width=15, textvariable=name_text)
        self.name_entry.grid(row=0, column=4)
        self.color_button = Button(self, bg=self.tile_color, text="    ",
                                   command=lambda: self.choose_color())
        self.color_button.grid(row=0, column=5, padx=2)
        self.fill_label = Label(self, text="fill:")
        self.fill_label.grid(row=0, column=6)
        fill_text = tk.StringVar()
        fill_text.set(self.tile_fill)
        self.fill_entry = Entry(self, width=4, textvariable=fill_text)
        self.fill_entry.grid(row=0, column=7)
        self.islands_label = Label(self, text="islands:")
        self.islands_label.grid(row=0, column=8)
        islands_text = tk.StringVar()
        islands_text.set(self.tile_islands)
        self.islands_entry = Entry(self, width=2, textvariable=islands_text)
        self.islands_entry.grid(row=0, column=9)

        self.edit_mode = False
        self.set_edit_mode(self.edit_mode)
        self.edit_button = Button(
            self, text="E", command=lambda: self.enter_edit_mode())
        self.edit_button.grid(row=0, column=10)
        self.save_button = Button(
            self, text="S", command=lambda: self.save_tile())

        self.add_button = Button(
            self, text="+", command=lambda: self.add_new_tile(root, level))
        self.add_button.grid(row=0, column=11)
        self.remove_button = Button(
            self, text="-", command=lambda: self.remove_tile())
        self.remove_button.grid(row=0, column=12)

    def add_new_tile(self, root, level):
        new_segment = TileInfoSegment(
            root, self.main_gui, self.tile_id, level=level+1)
        new_segment.enter_edit_mode()
        self.main_gui.insert_new_tile(new_segment, self.tile_id)
        self.main_gui.update_tiles_info()

    def remove_tile(self):
        to_remove = self.find_children_tiles()
        to_remove.append(self)

        for element in to_remove:
            self.main_gui.remove_tile_from_list(element)
            element.grid_forget()

        self.main_gui.update_tiles_info()

    def find_children_tiles(self):
        if self.tile_id == 0:  # handling not saved tiles that have id of 0
            return []  # returning empty list because 0 is root tile

        children_tiles = []
        parent_id = self.tile_id
        for tile in self.main_gui.tiles_info_list:
            if parent_id == tile.parent_tile_id:
                children_tiles.append(tile)
                children_tiles += tile.find_children_tiles()

        return children_tiles

    def enter_edit_mode(self):
        self.edit_mode = True
        self.set_edit_mode(self.edit_mode)
        self.edit_button.grid_forget()
        self.save_button.grid(row=0, column=10)
        self.add_button.config(state="disabled")

    def set_edit_mode(self, edit_mode=False):
        if edit_mode:
            state = "normal"
            button_state = "normal"
        else:
            state = "readonly"
            button_state = "disabled"
        self.id_entry.config(state=state)
        self.name_entry.config(state=state)
        self.fill_entry.config(state=state)
        self.islands_entry.config(state=state)
        self.color_button.config(state=button_state)

    def save_tile(self):
        try:
            self.validate_input()
            self.update_tile_data()
            self.edit_mode = False
            self.set_edit_mode(self.edit_mode)
            self.save_button.grid_forget()
            self.edit_button.grid(row=0, column=10)
            self.add_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Invalid tile data", str(e))

    def update_tile_data(self):
        self.tile_id = int(self.id_entry.get())
        self.tile_name = self.name_entry.get()
        self.tile_fill = float(self.fill_entry.get())
        self.tile_islands = int(self.islands_entry.get())

    def validate_input(self):
        """Checks if tile data provided by user is valid"""
        if len(self.id_entry.get()) == 0:
            raise EmptyFieldError("Tile ID must be provided")
        try:
            t_id = int(self.id_entry.get())
        except ValueError:
            raise ValueError("Tile ID must be integer")
        if not self.check_if_uniqe_id(t_id):
            raise NotUniqeIDError("Tile ID must be uniqe")
        if t_id < 0:
            raise ValueError("ID cannot be negative")

        if len(self.name_entry.get()) == 0:
            raise EmptyFieldError("Tile name must be provided")

        if len(self.fill_entry.get()) == 0:
            raise EmptyFieldError("Tile fill must be provided")
        try:
            t_fill = float(self.fill_entry.get())
        except ValueError:
            raise ValueError("Tile fill must be float")
        if t_fill < 0 or t_fill > 1:
            raise ValueError("Tile fill must be float from 0 to 1")

        if len(self.islands_entry.get()) == 0:
            raise EmptyFieldError("Tile islands number must be provided")
        try:
            t_islands = int(self.islands_entry.get())
        except ValueError:
            raise ValueError("Tile islands must be integer")
        if t_islands < 1:
            raise ValueError("Island number must be at least 1")

    def choose_color(self):
        color = colorchooser.askcolor()
        self.color_button.config(bg=color[1])
        self.tile_color = color[1]

    def construct_tile_object(self):
        tile = Tile(self.tile_id, self.tile_name, self.tile_color,
                    self.tile_fill, self.tile_islands)
        return tile

    def check_if_uniqe_id(self, t_id):
        for existing_tile in self.main_gui.tiles_info_list:
            if existing_tile.tile_id == t_id and not existing_tile.edit_mode:
                return False
        return True


class RootTileInfoSegment(TileInfoSegment):
    """
    Widget of root tile, less options of editing
    """

    def __init__(self, root, main_gui, name="ocean", color="blue"):
        TileInfoSegment.__init__(self, root, main_gui, 'root', tile_id=0,
                                 name="ocean", color="blue", fill=1, islands=1,
                                 level=0)
        self.remove_button.grid_forget()
        self.fill_label.grid_forget()
        self.fill_entry.grid_forget()
        self.islands_label.grid_forget()
        self.islands_entry.grid_forget()
        self.id_entry.config(state="disabled")

    def set_edit_mode(self, edit_mode=False):
        if edit_mode:
            state = "normal"
            button_state = "normal"
        else:
            state = "readonly"
            button_state = "disabled"
        self.name_entry.config(state=state)
        self.color_button.config(state=button_state)


class NotUniqeIDError(Exception):
    pass


class EmptyFieldError(Exception):
    pass


class TileInEditModeError(Exception):
    pass


class EmptyEntryFieldError(Exception):
    pass


if __name__ == "__main__":
    root = Tk()
    GenerationGUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
