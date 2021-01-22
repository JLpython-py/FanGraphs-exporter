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


.. py:class:: class WebDriver(self):

	.. py:attribute:: options
	
		The options returned after calling :py:func:`selenium.webdriver.firefox.options.Options`
		The default options used:

			* ``self.options.headless``: ``True``
			* ``self.options.preferences``: 
	
				* ``"browser.download.folderList"``: 2
				* ``"browser.download.manager.showWhenStarting"``: ``False``
				* ``"browser.download.dir"``: ``os.getcwd()``
				* ``"browser.helperApps.neverAsk.saveToDisk"``: ``"text/csv"``

.. py:class:: class FanGraphs(self, *, setting)

	:param str setting: The setting string which corresponds to the FanGraphs page
	
		+---------------------------+----------------------------------+
		| **FanGraphs Page Title**  | **Corresponding setting string** |
		+---------------------------+----------------------------------+
		| Major League Leaderboards | 'leaders'                        |
		+---------------------------+----------------------------------+
		| Projections               | 'projections'                    |
		+---------------------------+----------------------------------+

	:raises fgexporter.InvalidSettingError: If the ``setting`` argument is not recognized

		.. py:attribute:: address
		
			The URL which corresponds to the original FanGraphs page.
		
			+---------------------------+-------------------------------------------+
			| **FanGraphs Page Title**  | **Corresponding URL**                     |
			+---------------------------+-------------------------------------------+
			| Major League Leaderboards | https://fangraphs.com/leaders.aspx        |
			+---------------------------+-------------------------------------------+
			| Projections               | https://fangraphs.com/projections.aspx    |
			+---------------------------+-------------------------------------------+

		.. py:attribute:: selectors
		
			A dictionary with the CSS selectors for the data configuration category, stored by type.
		
		.. py:attribute:: webdriver
		
			Holds the :py:class:`WebDriver` instance.

		.. py:attribute:: browser

			References the :py:attr:`browser` attribute of :py:attr:`webdriver`.

	.. py:classmethod:: get_options(self, category)
	
		:param str category: The data configuration category
		:returns: List of valid options for ``category``
		:rtype: List[Str]
		:raises fgexporter.FanGraphs.InvalidCategoryError: If ``category`` is not recognized
	
	.. py:classmethod:: get_current(self, category)
	
		:param str category: The data configuration category
		:returns: Current option for ``category``
		:rtype: Str
		:raises fgexporter.FanGraphs.InvalidCategoryError: If ``category`` is not recognized
	
	.. py:classmethod:: config(self, **kwargs)
	
		:param kwargs: Data configurations
		:raises fgexporter.FanGraphs.InvalidCategoryError: If keyword is not recognized
		:raises fgexporter.FanGraphs.InvalidOptionError: If keyword argument is not recognized

		:Keyword Arguments:
			
			category (str): The data configuration option which corresponds to the category

				*Note that the keyword argument name is identical to the corresponding string value.*

	.. py:classmethod:: reset(self)
	
		Passes :py:attr:`address` to the :py:func:`get` method of :py:attr:`browser`
	
	.. py:classmethod:: location(self)
	
		Returns the address that the browser is current at.
	
		:return: :py:attr:`current_url` attribute of :py:attr:`browser`
		:rtype: Str
	
	.. py:classmethod:: end_task(self)
	
		Calls :py:meth:`quit` method of :py:attr:`browser`

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
