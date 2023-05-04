from tethys_sdk.base import TethysAppBase


class Ngen(TethysAppBase):
    """
    Tethys app class for Next Generation Water Model.
    """

    name = 'Next Generation Water Model'
    description = 'Visualize the next generation water model output.'
    package = 'ngen'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/icon.gif'
    root_url = 'ngen'
    color = '#003087'
    tags = ''
    enable_feedback = False
    feedback_emails = []