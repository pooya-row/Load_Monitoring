def property_selector(material: str, k_t: str) -> list:
    """
    Get ``a, b, c`` and ``d`` values of a given material in a given
    condition from the material library.

    :param material: selected material
    :param k_t: selected condition of material
    :return: a, b, c, d values
    """

    import os
    # par_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    mat_file = os.path.join(os.getcwd(), '../lib/mat_lib.json')
    mat_lib = load_material_lib('C:\\Users\\pooya.rowghanian\\Documents\\'
                                '02.Python\\Rainflow\\mat_lib.json')
    # mat_lib = load_material_lib(mat_file)
    return mat_lib[material][k_t]


def write_material_lib(data: dict,
                       j_file: str = 'mat_lib.json'):
    """
    Writes the input dictionary into the indicated json file.

    :param data: input dictionary containing material properties.
    :param j_file: the file where the ``data`` will be written into.
    :return: Nil.
    """
    import json
    from pathlib import Path

    with open(j_file, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)

    return f'library was written in "{Path(j_file).stem}".'


def load_material_lib(j_file) -> dict:
    """
    Reads the input json file into a dictionary.

    :param j_file: the library file to be read.
    :return: a dictionary object containing the data fo the input ``j_file``.
    """

    import json
    with open(j_file, 'r') as f:
        lib = json.load(f)
    return lib


def add_material_to_lib(new_mat_name: str,
                        k_t: dict[str: list],
                        lib_file: str = 'mat_lib.json'):
    """
    Writes a new material into an existing material library.

    :param new_mat_name: name of the nw material which is being added to
        the library file.
    :param k_t: a dictionary the keys of which are string entries indicating
        the material conditions and corresponding values are lists of
        length 4 containing `a, b, c, d` values of that particular condition.
    :param lib_file: the library file where the new material will be added to.
    :return: Nil.
    """
    from pathlib import Path
    # import os
    # par_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    # mat_file = os.path.join(par_dir, 'mat_lib.json')
    # mat_file = lib_file
    cur_lib = load_material_lib(lib_file)

    if new_mat_name in cur_lib.keys():
        print(f'"{new_mat_name}" already exists in "{Path(lib_file).stem}". '
              f'Nothing added. Select a different name and try again.')
    else:
        cur_lib[new_mat_name] = k_t
        write_material_lib(cur_lib)
        print(f'"{new_mat_name}" successfully added to '
              f'"{Path(lib_file).stem}".')


def delete_material_from_lib(mat_to_delete: str,
                             lib_file: str = 'mat_lib.json'):
    """
    Deletes the indicated material from the indicated material library file.

    Caution!
    -------
    This change is permanent and cannot be undone.

    :param mat_to_delete: name of the material to be deleted.
        This must match one of the existing materials in the ``lib_file``.
    :param lib_file: the library file where ``mat_to_delete``will be
        deleted from.

    :return: Nil.
    """
    from pathlib import Path

    cur_lib = load_material_lib(lib_file)

    if mat_to_delete in cur_lib.keys():
        del cur_lib[mat_to_delete]
        print(f'"{mat_to_delete}" as successfully deleted from '
              f'"{Path(lib_file).stem}".')
        write_material_lib(cur_lib)
    else:
        print(f'"{mat_to_delete}" does not exist in "{Path(lib_file).stem}". '
              f'Nothing Deleted. Check Spelling.')


# add_material_to_lib('test', {'no data': []}, 'mat_lib.json')
# delete_material_from_lib('test', 'mat_lib.json')

# mat_lib = {
#     '2014-T6 Aluminium': {
#         'Unnotched, Wrought, Longitudinal': [21.49, 9.44, 0., 0.67],
#         '1.6, Bar, Longitudinal': [10.56, 4.02, 20.2, 0.55],
#         '2.4, Bar, Longitudinal': [10.59, 4.36, 11.7, 0.52],
#         '3.4, Rolled & Extruded Bar, Longitudinal': [8.35, 3.10, 10.6, 0.52],
#         '2.4, Hand forging, Longi. & Transverse': [12.4, 5.95, 0., 0.],
#     },
#
#     '2024-T3 Aluminium': {
#         'Unnotched, Sheet, Longitudinal': [11.1, 3.97, 15.8, 0.56],
#         '1.5, Sheet, Longitudinal': [7.5, 2.13, 23.7, 0.66],
#         '2.0, Sheet, Longitudinal': [9.2, 3.33, 12.3, 0.68],
#         '4.0, Sheet, Longitudinal': [8.3, 3.30, 8.5, 0.66],
#         '5.0, Sheet, Longitudinal': [8.9, 3.73, 3.9, 0.56],
#     },
#
#     '2024-T4 Aluminium': {
#         'Unnotched, Wrought, Longitudinal': [20.83, 9.09, 0., 0.52],
#         '1.6 , Bar, Longitudinal': [12.25, 5.16, 18.7, 0.57],
#         '2.4, Bar, Longitudinal': [14.33, 6.35, 3.2, 0.48],
#         '3.4, Wrought, Longitudinal': [8.18, 2.76, 11.6, 0.52],
#     },
#
#     '2024-T42 Aluminium': {
#         'No data available': [],
#     },
#
#     '7075-T6 Aluminium': {
#         'Unnotched, Various forms, Longitudinal': [18.22, 7.77, 10.15, 0.62],
#         '1.6, Rolled bar, Longitudinal': [8.26, 2.62, 15.3, 0.525],
#         '3.4, Rolled bar, Longitudinal': [9.19, 3.646, 5.36, 0.386],
#         'Unnotched, Sheet, Longitudinal': [14.86, 5.80, 0., 0.49],
#         '1.5, Sheet, Longitudinal': [9.54, 3.52, 18.7, 0.49],
#         '2.0, Sheet, Longitudinal': [7.50, 2.46, 18.6, 0.54],
#         '4.0, Sheet, Longitudinal': [10.2, 4.63, 5.3, 0.51],
#         '5.0, Sheet, Longitudinal': [7.51, 2.92, 6.7, 0.58]
#     },
#
#     '7075-T73 Aluminium': {
#         'No data available': [],
#     },
#
#     '7075-T7351 Aluminium': {
#         'No data available': [],
#     },
#
#     'AISI 4130 Steel, Normalized': {
#         'Unnotched, Sheet, Longitudinal': [9.65, 2.85, 61.3, 0.41],
#         '1.5, Sheet, Longitudinal': [7.94, 2.01, 61.3, 0.88],
#         '2.0, Sheet, Longitudinal': [17.1, 6.49, 0., 0.86],
#         '4.0, Sheet, Longitudinal': [12.6, 4.69, 0., 0.63],
#         '5.0, Sheet, Longitudinal': [12.0, 4.57, 0., 0.56],
#     },
#
#     'AISI 4130 Steel, F\N{LATIN SUBSCRIPT SMALL LETTER T}\N{LATIN SUBSCRIPT SMALL LETTER U} = 180 ksi': {
#         'Unnotched, Sheet, Longitudinal': [20.3, 7.31, 0., 0.49],
#         '2.0, Sheet, Longitudinal': [8.87, 2.81, 41.5, 0.46],
#         '4.0, Sheet, Longitudinal': [12.4, 4.45, 0., 0.60],
#     },
#
# }
