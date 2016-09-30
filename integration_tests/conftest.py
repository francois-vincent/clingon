# encoding: utf-8


def pytest_addoption(parser):
    parser.addoption('--reset', action='store_true',
                     help="force remove image, ie force an image build or pull "
                          "(default: reuse existing image")
    parser.addoption('--keep-running', action='store_true',
                     help="keep the containers up for debug")
