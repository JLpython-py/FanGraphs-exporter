.. fgexporter documentation master file, created by
   sphinx-quickstart on Thu Jan 21 13:31:51 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================================
Welcome to the FanGraphs-exporter documentation!
================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

FanGraphs-exporter is completely open-source.

See this project's `GitHub Repository`_. See the `latest release`_.

.. _GitHub Repository: https://github.com/JLpython-py/FanGraphs-exporter
.. _latest release: https://github.com/JLpython-py/FanGraphs-exporter/releases

=============
API Reference
=============


.. py:class:: class fgexporter.WebDriver

	.. py:classmethod:: WebDriver.__init__(self)

		.. py:attribute:: options

			:returns: The `selenium.webdriver.firefox.options.Options`_ object

			The default options used:

				.. py:attribute:: headless: ``True``
				.. py:attribute:: preferences:

					* ``"browser.download.folderList"``: 2
					* ``"browser.download.manager.showWhenStarting"``: ``False``
					* ``"browser.download.dir"``: ``os.getcwd()``
					* ``"browser.helperApps.neverAsk.saveToDisk"``: ``"text/csv"``

			.. _selenium.webdriver.firefox.options.Options: https://selenium-python.readthedocs.io/api.html#selenium.webdriver.firefox.options.Options


.. py:exception:: InvalidSettingError

	Raised when the setting argument of :py:meth:`FanGraphs.__init__` is not recognized


.. py:class:: class fgexporter.FanGraphs


	.. py:classmethod:: FanGraphs.__init__(self, *, setting)

		:param str setting: The setting string which corresponds to the FanGraphs page

			+---------------------------+----------------------------------+
			| **FanGraphs Page Title**  | **Corresponding setting string** |
			+---------------------------+----------------------------------+
			| Major League Leaderboards | 'leaders'                        |
			+---------------------------+----------------------------------+
			| Projections               | 'projections'                    |
			+---------------------------+----------------------------------+

		:raises :py:exc:`fgexporter.InvalidSettingError`: If the ``setting`` argument is not recognized


		.. py:attribute:: address

			:returns: The URL which corresponds to the initial FanGraphs page

				+---------------------------+-------------------------------------------+
				| **FanGraphs Page Title**  | **Corresponding URL**                     |
				+---------------------------+-------------------------------------------+
				| Major League Leaderboards | https://fangraphs.com/leaders.aspx        |
				+---------------------------+-------------------------------------------+
				| Projections               | https://fangraphs.com/projections.aspx    |
				+---------------------------+-------------------------------------------+


		.. py:attribute:: selectors

			:returns: A dictionary with the CSS selectors for the data configuration categories, stored by type.
			:rtype: Dict


		.. py:attribute:: webdriver

			:returns: The :py:class:`WebDriver` instance.


		.. py:attribute:: browser

			:returns: The :py:attr:`browser` attribute of :py:attr:`webdriver`.


	.. py:exception:: InvalidCategoryError

		Raised when the data configuration category is invalid


	.. py:exception:: InvalidOptionError

		Raised when the data configuration option is invalid


	.. py:classmethod:: get_options(self, category)
	
		:param str category: The data configuration category
		:returns: List of valid options for ``category``
		:rtype: List[Str]
		:raises FanGraphs.InvalidCategoryError: If ``category`` is not recognized

	
	.. py:classmethod:: get_current(self, category)
	
		:param str category: The data configuration category
		:returns: Current option for ``category``
		:rtype: Str
		:raises FanGraphs.InvalidCategoryError: If ``category`` is not recognized

	
	.. py:classmethod:: config(self, **kwargs)
	
		:param kwargs: Data configurations
		:raises FanGraphs.InvalidCategoryError: If keyword is not recognized
		:raises FanGraphs.InvalidOptionError: If keyword argument is not recognized

		:Keyword Arguments:
			
			category (str): The data configuration option which corresponds to the category. Use :py:meth:`get_options` to get possible options.

				*Note that the keyword argument name is identical to the corresponding string value.*


	.. py:classmethod:: reset(self)
	
		Passes :py:attr:`address` to the `get`_ method of :py:attr:`browser`
		
		.. _`get`: https://selenium-python.readthedocs.io/api.html#selenium.webdriver.remote.webdriver.WebDriver.get


	.. py:classmethod:: location(self)
	
		Returns the address that the browser is current at.
	
		:return: `current_url`_ attribute of :py:attr:`browser`
		:rtype: Str
	
		.. _`current_url`: https://selenium-python.readthedocs.io/api.html#selenium.webdriver.remote.webdriver.WebDriver.current_url


	.. py:classmethod:: end_task(self)
	
		Calls `quit`_ method of :py:attr:`browser`

		.. _`quit`: https://selenium-python.readthedocs.io/api.html#selenium.webdriver.firefox.webdriver.WebDriver.quit


	.. py:classmethod:: export(self)
	
		Downloads the configured data as a CSV file to the current working directory.
		The directory which the file is downloaded to can be altered with the ``"browser.download.dir"`` preference.
		The file will be named the formatted current time: ``datetime.datetime.now().strftime('%d.%m.%y %H.%M.%S')``

		:returns: Name of exported file
		:rtype: Str


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
