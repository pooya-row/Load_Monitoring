import PySimpleGUI as Sg
from utils.material_lib import load_material_lib
import os
import ctypes
import platform


def make_dpi_aware():
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)


make_dpi_aware()


def gui_single_file():
    # Sg.change_look_and_feel('DarkGrey4')
    current_path = 'C:\\Users\\pooya.rowghanian\\Desktop\\New folder' \
                   '\\Monday November 15, 2021 01-04 PM.dat'
    # current_path = os.getcwd() + '\\signal.csv'
    # par_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    # logo file location
    logo_file = os.path.join(os.path.dirname(__file__),
                             '..\\Images\\logo.png')

    # Load material library
    mat_lib = load_material_lib(os.path.join(os.path.dirname(__file__),
                                             '..\\ilb\\mat_lib.json'))
    materials = list(mat_lib.keys())

    left_column = [
        [Sg.T('Signal File', pad=((0, 0), (8, 0)))],
        [Sg.T('Mean bin size', pad=((0, 0), (6, 0)))],
        [Sg.T('Range bin size', pad=((0, 0), (6, 0)))],
        [Sg.T('g-exceedance Resolution', pad=((0, 0), (6, 0)))],
        [Sg.T('Material', pad=((0, 0), (6, 0)))],
        [Sg.T('K\N{LATIN SUBSCRIPT SMALL LETTER T}', pad=((0, 0), (7, 20)))],
    ]

    right_column = [
        [Sg.I(default_text=current_path, size=(30, 1), key='-FILE-'),
         Sg.FileBrowse(font=('Microsoft YaHei UI', 9))],
        [Sg.I(default_text='0.25', size=(30, 1), key='-MBS-')],
        [Sg.I(default_text='0.25', size=(30, 1), key='-RBS-')],
        [Sg.I(default_text='0.1', size=(30, 1), key='-gRES-')],
        [Sg.Combo(values=materials, default_value=materials[0], size=(30, 1),
                  key='-MATERIAL-', readonly=True, enable_events=True)],
        [Sg.Combo(values=list(mat_lib[materials[0]].keys()),
                  default_value=list(mat_lib[materials[0]].keys())[1],
                  size=(30, 1), key='-KT-', readonly=True)]
    ]

    layout = [
        [Sg.Column(left_column, vertical_alignment='top',
                   element_justification='right'),
         Sg.Column(right_column, vertical_alignment='top')],
        [Sg.B('Submit', focus=True), Sg.B('Cancel'),
         Sg.T(
             '                                                                     '),
         Sg.Image(filename=logo_file, key='-LOGO-')]
    ]

    wdw = Sg.Window('Damage Analysis', layout, font=('Microsoft YaHei UI', 11))

    while True:
        event, value = wdw.read()

        if event in ['Cancel', 'Escape:27']:
            print('Interrupted by the user.')
            exit()

        if event == Sg.WIN_CLOSED:
            break

        if event == '-MATERIAL-':
            mat = value['-MATERIAL-']
            wdw['-KT-'].update(values=list(mat_lib[mat].keys()),
                               set_to_index=0)

        if event == 'Submit':
            m_bs = value['-MBS-']
            r_bs = value['-RBS-']
            ge_bs = value['-gRES-']
            file_path = value['-FILE-']
            material = value['-MATERIAL-']
            k_t = value['-KT-']

            if value['-KT-'] == 'No data available':
                ppw = Sg.popup_ok_cancel(
                    f'The built-in Material Library does not contain any '
                    f'valid K\N{LATIN SUBSCRIPT SMALL LETTER T} value'
                    f' for {material}.\n\n- Click "Cancel" to select a '
                    f'different material, or\n\n'
                    f'- Click "OK" to continue without a material '
                    f'selection. This will deactivate the total damage '
                    f'evaluation feature.\n',
                    title='Invalid K\N{LATIN SUBSCRIPT SMALL LETTER T}',
                    button_color=('#FFFFFF', '#283B5B'),
                    background_color='#C2C2C2',
                    text_color='black',
                    font=('Microsoft YaHei UI', 11))

                if ppw in ['Cancel', Sg.WIN_CLOSED]:
                    continue

            wdw.close()

    wdw.finalize()

    return float(m_bs), float(r_bs), float(ge_bs), file_path, material, k_t


def call_gui() -> (bool, float, float, float, str, str, str, bool, float):
    """
    This is a user interface which allows for
     1. selecting the type of analysis: single IMU files or multiple IMU files.
     2. setting analysis parameters

    :return: A tuple which contains the following, respectively:
        1. mode of analysis: single file or multiple;
        2. mean bin size
        3. range bin size
        4. g-exceedance bin size (resolution)
        5. the address of the file or files to be analyzed
        6. the material selected for stress evaluation (Minor's rule)
        7. configuration of the material the Kt value is based on for stress
           evaluation (Minor's rule)
        8. whether to filter the input data or not
        9. if 8 is True, the minimum amplitude which will remain intact
           during filtration

    """

    # initial default values
    current_dir = 'C:\\Users\\pooya.rowghanian\\Desktop\\New Folder'
    current_file = 'C:\\Users\\pooya.rowghanian\\Desktop\\New Folder\\' \
                   'Wednesday November 10, 2021 12-33 PM.dat'

    # location of logo
    logo_file = os.path.join(os.path.dirname(__file__),
                             '..\\Images\\logo.png')

    # location of material library
    mat_file = os.path.join(os.path.dirname(__file__),
                            '..\\lib\\mat_lib.json')

    # read material library
    mat_lib = load_material_lib(mat_file)
    materials = list(mat_lib.keys())

    # buttons to be centered in the layout
    b_row = [[Sg.B('OK', focus=True, s=(9, 1)), Sg.B('Cancel', s=(9, 1))]]

    # layout of the analysis type window
    init_layout = [
        [Sg.T('What do you want to do?')],
        [Sg.Radio('Process a single flight IMU data', 'num_of_files',
                  default=False)],
        [Sg.Radio('Process multiple flights IMU data', 'num_of_files',
                  default=True, key='-MLT FIL-')],
        [Sg.Column(b_row, justification='center')]
    ]

    # analysis type window
    init_wdw = Sg.Window('Analysis Type', init_layout,
                         font=('Microsoft YaHei UI', 11),
                         return_keyboard_events=True)

    while True:
        event, value = init_wdw.read()

        # termination of the windows
        if event in ['Cancel', Sg.WIN_CLOSED, 'Escape:27']:
            print('Terminated by the user.')
            exit()

        # when OK clicked `mode` is set based on user selection
        if event == 'OK':
            if value['-MLT FIL-']:
                multiple_files = True
            else:
                multiple_files = False
            break

    init_wdw.close()
    init_wdw.finalize()

    # set analysis window parameters based on `mode`
    if multiple_files:  # multiple file mode
        # is used in `left_column`
        first_t = [Sg.T('Signal Files Directory', pad=((0, 0), (8, 0)))]
        # is used in `right_column`
        first_IN = [Sg.I(default_text=current_dir, size=(30, 1), key='-DIR-'),
                    Sg.FolderBrowse(font=('Microsoft YaHei UI', 10), s=(7, 1))]
    else:  # single file mode
        first_t = [Sg.T('Signal File', pad=((0, 0), (8, 0)))]
        first_IN = [Sg.I(default_text=current_file, size=(30, 1), key='-DIR-'),
                    Sg.FileBrowse(font=('Microsoft YaHei UI', 10), s=(7, 1))]

    # design of analysis window
    left_column = [
        first_t,
        [Sg.T('Mean bin size', pad=((0, 0), (6, 0)))],
        [Sg.T('Range bin size', pad=((0, 0), (6, 0)))],
        [Sg.T('g-exceedance Resolution', pad=((0, 0), (6, 0)))],
        [Sg.T('Material', pad=((0, 0), (6, 0)))],
        [Sg.T('K\N{LATIN SUBSCRIPT SMALL LETTER T}', pad=((0, 0), (7, 20)))],
    ]

    right_column = [
        first_IN,
        [Sg.I(default_text='0.1', size=(30, 1), key='-MBS-')],
        [Sg.I(default_text='0.1', size=(30, 1), key='-RBS-')],
        [Sg.I(default_text='0.05', size=(30, 1), key='-gRES-')],
        [Sg.Combo(values=materials, default_value=materials[0], size=(30, 1),
                  key='-MATERIAL-', readonly=True, enable_events=True)],
        [Sg.Combo(values=list(mat_lib[materials[0]].keys()),
                  default_value=list(mat_lib[materials[0]].keys())[1],
                  size=(30, 1), key='-KT-', readonly=True)],
        [Sg.CB('Apply Racetrack Filter on Raw Data', default=True,
               key='-RTF-', enable_events=True)],
        [Sg.T('Keep Amplitudes Above', pad=((28, 0), (0, 0))),
         Sg.I(default_text='0.10', size=(4, 1), key='-hVALUE-'), Sg.T('g')],
        [Sg.CB('Show Labels on the Plot', key='-SL-')]
    ]

    layout = [
        [Sg.Column(left_column, vertical_alignment='top',
                   element_justification='right'),
         Sg.Column(right_column, vertical_alignment='top')],
        [Sg.B('Submit', focus=True, s=(9, 1)), Sg.B('Cancel', s=(9, 1)),
         Sg.T('                                                      '),
         Sg.Image(filename=logo_file, key='-LOGO-')]
    ]

    # analysis window
    wdw = Sg.Window('Damage Analysis', layout, font=('Microsoft YaHei UI', 11),
                    return_keyboard_events=True, size=(950, 520))

    while True:
        event, value = wdw.read()

        # termination by user
        if event in ['Cancel', 'Escape:27']:
            print('Interrupted by the user.')
            exit()

        # termination of while loop
        if event == Sg.WIN_CLOSED:
            break

        # change of material updates corresponding Kt configs and selects
        # the first available one
        if event == '-MATERIAL-':
            wdw['-KT-'].update(
                values=list(mat_lib[value['-MATERIAL-']].keys()),
                set_to_index=0)

        # when checkbox is (de)activated
        if event == '-RTF-':
            if not value['-RTF-']:
                wdw['-hVALUE-'].update(disabled=True, text_color='grey')
            else:
                wdw['-hVALUE-'].update(disabled=False, text_color='black')

        # when `submit` is clicked
        if event == 'Submit':
            m_bs = value['-MBS-']
            r_bs = value['-RBS-']
            ge_bs = value['-gRES-']
            dir_path = value['-DIR-']
            material = value['-MATERIAL-']
            k_t = value['-KT-']
            rt_filter = value['-RTF-']
            h = value['-hVALUE-']
            show_labels = value['-SL-']

            # when material data is not available in the library user has
            # the choice to change the material or proceed with no material
            if value['-KT-'] == 'No data available':
                ppw = Sg.popup_ok_cancel(
                    f'The built-in Material Library does not contain any '
                    f'valid K\N{LATIN SUBSCRIPT SMALL LETTER T} value'
                    f' for {material}.\n\n- Click "Cancel" to select a '
                    f'different material, or\n\n'
                    f'- Click "OK" to continue without a material '
                    f'selection. This will deactivate the total damage '
                    f'evaluation feature.\n',
                    title='Invalid K\N{LATIN SUBSCRIPT SMALL LETTER T}',
                    button_color=('#FFFFFF', '#283B5B'),
                    background_color='#C2C2C2',
                    text_color='black',
                    font=('Microsoft YaHei UI', 11))

                # termination of the popup window
                if ppw in ['Cancel', Sg.WIN_CLOSED, 'Escape:27']:
                    continue

            wdw.close()

    wdw.finalize()

    return multiple_files, float(m_bs), float(r_bs), \
           float(ge_bs), dir_path, material, k_t, rt_filter, float(h), \
           show_labels
