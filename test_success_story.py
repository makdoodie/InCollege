import pytest
from system import System, Menu
from unittest import mock


@pytest.fixture
def system_instance():
  return System()


def test_video_option(system_instance, capsys):
  # initialize menu options
  system_instance.initMenu()

  # access homePage attribute
  home_page = system_instance.homePage

  # check if video option is available
  assert '5' in home_page.selections, "Selection '5' not found in home page options"
  assert home_page.selections['5'] == {
    'label': 'See Our Success Video',
    'action': system_instance.video_menu
  }

  # simulate user choosing video option
  with mock.patch('builtins.input', side_effect=['5', '0', '0']):
    system_instance.home_page()

  # capture output
  captured = capsys.readouterr()

  # assert expected output
  assert "(Playing Video)" in captured.out


def test_student_success(system_instance, capsys):
  # initialize menu options
  system_instance.initMenu()

  # access homePage attribute
  home_page = system_instance.homePage

  success_story = """
      Welcome To The InCollege Home Page!
      
      The Place Where Students Take The Next Big Step.

      "I Had To Battle With Anxiety Every Day Until I Signed Up For InCollege.
       Now, My Future Is On The Right Track And Im Able To Apply My Education To My 
       Dream Career. Finding A Place In My Field Of Study Was A Breeze"
        - InCollege User

    """

  assert home_page.opening == success_story

 