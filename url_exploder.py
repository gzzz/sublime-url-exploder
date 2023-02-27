import sublime, sublime_plugin, re

try:
	from urllib.parse import quote, unquote

	def _unquote(arg, as_is=False):
		if arg is None:
			return arg

		return unquote(arg)
except ImportError:
	from urllib       import quote, unquote

	def _unquote(arg, as_is=False):
		if arg is None:
			return arg

		if not as_is:
			arg = arg.decode('utf-8').encode('ascii')

		return unquote(arg).decode('utf-8')

def _quote(arg, as_is=False):
	if arg is None:
		return arg

	if not as_is:
		arg = arg.encode('utf-8')

	return quote(arg, safe='')


class URLExploder(object):
	def __init__(self, view):
		self.view = view


	def explode(self, edit, as_is=False):
		view = self.view
		selections = view.sel()

		if len(selections) == 1 and selections[0].empty():
			selections = view.split_by_newlines(sublime.Region(0, view.size()))

		for region in selections:
			if region.empty():
				region = view.line(region)

			view.replace(edit, region, self._explode(view.substr(region), as_is))


	def implode(self, edit, as_is=False):
		view = self.view
		selections = view.sel()

		if len(selections) == 1 and selections[0].empty():
			selections = []
			lines = view.split_by_newlines(sublime.Region(0, view.size()))
			region = (0, 0)

			for line in lines:
				text = view.substr(line)

				if not line.empty() and text[0] in ['?', '&', '#']:
					region = (region[0], line.end())
				else:
					selections.append(sublime.Region(region[0], region[1]))
					region = (line.begin(), line.begin())

			selections.append(sublime.Region(region[0], region[1]))

		for region in selections:
			if region.empty():
				continue

			view.replace(edit, region, self._implode(view.substr(region), as_is))

	def _explode(self, url, as_is=False):
		result, query_string, fragment = self._parse_imploded_url(url, as_is)

		for qs in query_string:
			result += '\n?' + '\n&'.join(qs)

		if fragment:
			if not as_is:
				fragment = _unquote(fragment, as_is)

			result += '\n#' + fragment

		return result

	def _implode(self, url, as_is=False):
		result, query_string, fragment = self._parse_exploded_url(url, as_is=True)

		for qs in query_string:
			result += '?' + '&'.join(['='.join(filter(None, self._mold_query_string_param(name, value, as_is))) for param in qs for (name, value) in self._parse_query_string_param(param)])

		if fragment:
			if not as_is:
				fragment = _quote(fragment, as_is)

			result += '#' + fragment

		return result

	def _parse_imploded_url(self, url, as_is=False):
		url = url.strip()
		base = fragment = ''

		if '#' in url:
			url_parts = url.split('#')

			fragment = url_parts[1]
			url = url_parts[0]

		url_parts = url.split('?')
		base = url_parts[0]
		query_string = [self._parse_query_string(url_parts[part], as_is) for part in range(1, len(url_parts))]

		return base, query_string, fragment

	def _parse_exploded_url(self, url, as_is=False):
		url = url.strip()
		# url = re.sub('[^\S\n]+', '', url)
		url = re.sub('\n+', '\n', url)
		url = url.split('\n')

		base = fragment = ''
		query_string = []

		if url:
			target = []

			if url[0][0] not in ['?', '&', '#']:
				base = url[0]

				del url[0]

			if url[-1][0] == '#':
				fragment = url[-1][1:]

				del url[-1]

			for param in url:
				if param[0] == '?':
					target = []
					query_string.append(target)

				target.append(param[1:])

			query_string = self._parse_query_string(query_string, as_is=as_is, only_first_param=True)

		return base, query_string, fragment

	def _parse_query_string(self, query_string, as_is=False, only_first_param=False):
		maxsplit = -1
		if only_first_param:
			maxsplit = 1

		if query_string:
			if type(query_string) is not list:
				query_string = [part for part in query_string.split('&', maxsplit)]

			if not as_is:
				query_string = [_unquote(part, as_is) for part in query_string]
				query_string.sort()

			return query_string
		else:
			return []

	def _mold_query_string_param(self, name, value, as_is=False):
		if not as_is:
			return (_quote(name), _quote(value))
		else:
			return (name, value)

	def _parse_query_string_param(self, param):
		param = param.split('=', 1)

		if len(param) == 1:
			param.append(None)

		return [param]


class URLCommand(sublime_plugin.TextCommand):
	def __init__(self, *args):
		super(URLCommand, self).__init__(*args)

		self.exploder = URLExploder(self.view)


class ExplodeUrlCommand(URLCommand):
	def run(self, edit):
		self.exploder.explode(edit)


class ExplodeUrlAsIsCommand(URLCommand):
	def run(self, edit):
		self.exploder.explode(edit, as_is=True)


class ImplodeUrlCommand(URLCommand):
	def run(self, edit):
		self.exploder.implode(edit)


class ImplodeUrlAsIsCommand(URLCommand):
	def run(self, edit):
		self.exploder.implode(edit, as_is=True)