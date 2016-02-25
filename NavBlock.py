import sublime, sublime_plugin, re

class NavBlockCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		sels = self.view.sel()
		if not sels :
			return

		cursor = sels[0].begin()

		search_lines = None
		if args['dir'] == 'up' :
			search_region = sublime.Region(0, cursor)
			search_lines = self.view.lines(search_region)
			search_lines.reverse()
		else :
			search_region = sublime.Region(cursor, self.view.size())
			search_lines = self.view.lines(search_region)

		target_line = search_lines.pop(0)

		for search_line in search_lines :
			line = self.view.substr(search_line)

			if "//" in line :
				continue

			if (('{' in line and not '}' in line)
			   or ('}' in line and not '{' in line)) :
				target_line = search_line
				break

		position = target_line.end()

		# Sets the cursor to position
		sels.clear()
		sels.add(position)
		self.view.show(target_line)
