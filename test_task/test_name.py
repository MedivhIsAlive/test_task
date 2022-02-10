import pytest
import pytest_mock
from scanner_handler import CheckQr


class DataClass:
    qrs_right = [i * "1" for i in (3, 5, 7)]
    qrs_wrong = [i * "1" for i in (1, 2, 4, 12)]
    ids_right = [f"Len: {len(i)}|" for i in qrs_right]
    ids_wrong = [f"Len: {len(i)}" for i in qrs_wrong]


@pytest.mark.parametrize("data_right", DataClass.qrs_right, ids=DataClass.ids_right)
def test_color_right(mocker, data_right):
    mocker.patch.object(CheckQr, "check_in_db", return_value=True)
    mocker.patch.object(CheckQr, "can_add_device")
    code = CheckQr()
    qr = data_right
    code.check_scanned_device(qr)
    colors = {
        3: 'Red',
        5: 'Green',
        7: 'Fuzzy Wuzzy'
    }
    code.can_add_device.assert_called_once_with(f"hallelujah {qr}")
    assert code.color == colors.get(len(qr))


@pytest.mark.parametrize("data_wrong", DataClass.qrs_wrong, ids=DataClass.ids_wrong)
def test_color_wrong(data_wrong, mocker):
    mocker.patch.object(CheckQr, "check_in_db", return_value=True)
    mocker.patch.object(CheckQr, "send_error")
    code = CheckQr()
    qr = data_wrong
    code.check_scanned_device(qr)
    code.send_error.assert_called_once_with(f"Error: Wrong qr length {len(qr)}")
    assert (code.color is None)


def test_db(mocker):
    mocker.patch.object(CheckQr, "check_in_db", return_value=None)
    mocker.patch.object(CheckQr, "send_error")
    code = CheckQr()
    code.check_scanned_device("123")
    code.send_error.assert_called_once_with("Not in DB")
