import re


class Remapper:
    """
    Path remapping module

    :func:`remap` takes as an input a list of paths to remap and a platform name and returns list of paths remapped
     according to the map.
    """

    def __init__(self, map):
        """
        :type map: {String: list}
        """
        self._map = self.check_map(map)

    def remap(self, paths, output_platform):
        """
        Remaps given paths to given output platform if the platform name can be found in the map.
        If the input path is entered in the map more than once, the first one in the list will be used.


        :type paths: list
        :type output_platform: String
        :rtype: list
        """
        if output_platform not in self._map.keys():
            print 'Error: platform name {} not found in map'.format(output_platform)
        remapped_paths = []
        for path in paths:
            path = path.replace('\\', '/')
            if self.check_path(path):
                remapped_paths.append(self.remap_path(path, output_platform))
            else:
                print 'invalid path: {}'.format(path)
        return remapped_paths

    def remap_path(self, input_path, output_platform):
        """
        Remaps a path from the input according to the map.

        :type input_path: String
        :type output_platform: String
        :rtype: String
        """
        for platform, platform_paths in self._map.iteritems():
            if platform != output_platform:
                for i in xrange(len(platform_paths)):
                    if input_path.startswith(platform_paths[i]):
                        remainder = input_path.split(platform_paths[i])[1]
                        new_prefix = self._map[output_platform][i]
                        if not new_prefix.endswith('/') and not remainder.startswith('/'):
                            new_prefix += '/'
                        return new_prefix + remainder
        return input_path

    def check_map(self, map):
        """
        Checks if paths in map are correct and eventually corrects style of a path.

        :type map: {String: list}
        :rtype: {String: list}
        """
        for platform, paths in map.iteritems():
            map[platform] = [path.replace('\\', '/') for path in paths]
            for path in paths:
                self.check_path(path)
        return map

    @staticmethod
    def check_path(path):
        """
        Checkes if path format is correct.
        :type path: String
        :rtype: Boolean
        """
        pattern = re.compile('(\\\\?([^\\/]*[\\/])*)([^\\/]+)$')
        return True if re.match(pattern, path) else False
