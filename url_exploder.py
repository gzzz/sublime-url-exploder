import sublime, sublime_plugin

try:
	from urllib.parse import quote, unquote
except ImportError:
	from urllib       import quote, unquote


class URLExploder(object):
	def __init__(self, view):
		self.view = view

	def process(self, edit, processor, as_is=False):
		view = self.view

		for region in view.sel():
			if region.empty():
				region = sublime.Region(0, view.size())

			view.replace(edit, region, processor(view.substr(region), as_is))

	def explode(self, url, as_is=False):
		result, query_string, fragment = self._parse_url(url, as_is)

		for qs in query_string:
			result += '\n?' + '\n&'.join(qs)

		if fragment:
			result += '\n#' + fragment

		return result

	def collapse(self, url, as_is=False):
		result, query_string, fragment = self._parse_url(url.replace('\n', ''), as_is=True)

		for qs in query_string:
			result += '?' + '&'.join(['%s=%s' % self._mold_query_string_param(name, value, as_is) for param in qs for (name, value) in [param.split('=')]])

		if fragment:
			result += '#' + fragment

		return result

	def _parse_url(self, url, as_is=False):
		if not as_is:
			url = url.encode('ascii')

		fragment = ''
		if '#' in url:
			url_parts = url.split('#')

			fragment = url_parts[1]
			url = url_parts[0]

		url_parts = url.split('?')
		base = url_parts[0]
		query_string = []

		for part in xrange(1, len(url_parts)):
			query_string.append(self._parse_query_string(url_parts[part], as_is))

		return base, query_string, fragment

	def _parse_query_string(self, query_string, as_is=False):
		if query_string != '':
			query_string = [part for part in query_string.split('&')]

			if not as_is:
				query_string = [unquote(part).decode('utf-8') for part in query_string]
				query_string.sort()

			return query_string

	def _mold_query_string_param(self, name, value, as_is=False):
		if not as_is:
			return (quote(name.encode('utf-8')), quote(value.encode('utf-8')))
		else:
			return (name, value)


class URLCommand(sublime_plugin.TextCommand):
	def __init__(self, *args):
		super(URLCommand, self).__init__(*args)

		self.exploder = URLExploder(self.view)


class ExplodeUrlCommand(URLCommand):
	def run(self, edit):
		self.exploder.process(edit, self.exploder.explode)


class ExplodeUrlAsIsCommand(URLCommand):
	def run(self, edit):
		self.exploder.process(edit, self.exploder.explode, as_is=True)


class CollapseUrlCommand(URLCommand):
	def run(self, edit):
		self.exploder.process(edit, self.exploder.collapse)


class CollapseUrlAsIsCommand(URLCommand):
	def run(self, edit):
		self.exploder.process(edit, self.exploder.collapse, as_is=True)