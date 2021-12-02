from pathlib import Path
import json
import os

def property_selector(material: str, k_t: str) -> list:
    """
    Get ``a, b, c`` and ``d`` values of a given material in a given
    condition from the material library.

    :param material: selected material
    :param k_t: selected condition of material
    :return: a, b, c, d values
    """

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

    with open(j_file, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)

    return f'library was written in "{Path(j_file).stem}".'


def load_material_lib(j_file) -> dict:
    """
    Reads the input json file into a dictionary.

    :param j_file: the library file to be read.
    :return: a dictionary object containing the data fo the input ``j_file``.
    """

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
