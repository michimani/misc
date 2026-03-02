import glob
import os
import re

FILE_TYPE = 'png'
NEW_FILE_PATTERN = r'.*(\d{4})-(\d{2})-(\d{2})_(?:at_)?\d{5,6}([^\/]+)?\.' + FILE_TYPE
SC_DIR = '/Users/michimani/Pictures/__ss_tmp'
SC_OUT_DIR = '/Users/michimani/Pictures/ScreenShots'

DIR_TYPE = 'MONTH'  # "DAY" or "MONTH"


def get_screen_captures():
    # type: () -> list(str)
    return glob.glob(SC_DIR + '/*.' + FILE_TYPE)


def rename_file_path(filename):
    # type: (str) -> str
    """Rename file path.

        * replace half space to under score
        * remove period
        * replace "(N)" of "（N）" to "_N"

        Example:
           "sc 2020-03-05_21.39.57.png" -> "sc_2020-03-05_213957.png"
    """
    filename_tmp = filename.replace('.' + FILE_TYPE, '')
    filename_tmp = re.sub(
        r'( |\(|（)', '_', re.sub(r'(\.|\)|）)', '', filename_tmp))
    return filename_tmp + '.' + FILE_TYPE


def create_daily_directory(filename):
    # type: (str) -> str
    """Create daily directory from renamed file name if it does not exists.

        Example:
            If the file name is "sc_2020-03-05_213957.png",
            following directories will be created.

            SC_OUT_DIR/2020/03/05
    """
    daily_dir = SC_OUT_DIR + \
        re.sub(NEW_FILE_PATTERN, r'/\1/\2/\3', filename)
    if os.path.exists(daily_dir) is False:
        print('create directory ' + daily_dir)
        os.makedirs(daily_dir)

    return daily_dir


def create_monthly_directory(filename):
    # type: (str) -> str
    """Create monthly directory from renamed file name if it does not exists.

        Example:
            If the file name is "sc_2020-03-05_213957.png",
            following directories will be created.

            SC_OUT_DIR/2020/03
    """
    monthly_dir = SC_OUT_DIR + \
        re.sub(NEW_FILE_PATTERN, r'/\1/\2', filename)
    if os.path.exists(monthly_dir) is False:
        os.makedirs(monthly_dir)

    return monthly_dir


def move_file(old_path, new_path):
    # type: (str, str) -> ()
    os.rename(old_path, new_path)
    print("'{str(new_path)}' moved.")


if __name__ == '__main__':
    sc_list = get_screen_captures()
    if len(sc_list) == 0:
        print('There are no scren capure file.')
        exit

    for sc_file_path in sc_list:
        renamed_file_path = rename_file_path(sc_file_path)
        if DIR_TYPE == 'DAY':
            out_dir = create_daily_directory(renamed_file_path)
        else:
            out_dir = create_monthly_directory(renamed_file_path)

        new_file_path = renamed_file_path.replace(SC_DIR, out_dir)
        move_file(sc_file_path, new_file_path)