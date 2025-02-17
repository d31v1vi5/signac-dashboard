# Copyright (c) 2022 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
from flask import Markup, render_template

from signac_dashboard.module import Module

try:
    import markdown

    MARKDOWN = True
except ImportError:
    MARKDOWN = False


class TextDisplay(Module):
    """Render custom text or Markdown in a card.

    This module calls a user-provided function to display text or Markdown
    content in a card. Rendering Markdown requires the :code:`markdown`
    library to be installed. Example:

    .. code-block:: python

        from signac_dashboard.modules import TextDisplay

        def my_text(job):
            return f"This job id is {job}."

        modules = [TextDisplay(message=my_text)]

    :param context: Supports :code:`'JobContext'` and :code:`'ProjectContext'`.
    :type context: str
    :param message: A callable accepting one argument of type
        :py:class:`signac.job.Job` or :py:class:`signac.Project`
        and returning text or Markdown content.
    :type message: callable
    :param markdown: Enables Markdown rendering if True (default: :code:`False`).
    :type markdown: bool
    """

    _supported_contexts = {"JobContext", "ProjectContext"}

    def __init__(
        self,
        name="Text Display",
        context="JobContext",
        message=lambda job_or_project: "No message provided.",
        markdown=False,
        **kwargs,
    ):
        super().__init__(
            name=name,
            context=context,
            template="cards/text_display.html",
            **kwargs,
        )
        self.message = message
        self.markdown = markdown

    def get_cards(self, job_or_project):
        msg = self.message(job_or_project)
        if self.markdown:
            if MARKDOWN:
                msg = Markup(
                    markdown.markdown(msg, extensions=["markdown.extensions.attr_list"])
                )
            else:
                msg = "Error: Install the 'markdown' library to render Markdown."
        return [{"name": self.name, "content": render_template(self.template, msg=msg)}]
