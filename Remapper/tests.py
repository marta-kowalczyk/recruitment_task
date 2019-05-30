import unittest

from remapper import Remapper


class TestSum(unittest.TestCase):

    def test_remapping(self):
        map = {'From': ['L:\\', 'P:\project1\\textures'],
               'To': ['X:\\', 'Z:\library\\textures']}
        remaper = Remapper(map)

        input = ['L:\\temp',
                 'P:/project1/textures\grass.tga',
                 'P:\project1\\assets\env\Forest',
                 'cache\Tree.abc']

        output = remaper.remap(input, 'To')
        expected_output = [
            'X:/temp',
            'Z:/library/textures/grass.tga',
            'P:/project1/assets/env/Forest',
            'cache/Tree.abc'
        ]

        self.assertEqual(output, expected_output)

    def test_remapping_different_platforms_or_path_styles_styles(self):
        map = {'Windows': ['L:\\', 'P:\\'],
               'Mac': ['/Volumes/l', '/Volumes/p']}
        remaper = Remapper(map)

        input = ['L:\\temp',
                 'P:/project1/textures\grass.tga',
                 'P:\project1\\assets\env\Forest',
                 'cache\Tree.abc']

        output = remaper.remap(input, 'Mac')
        expected_output = [
            '/Volumes/l/temp',
            '/Volumes/p/project1/textures/grass.tga',
            '/Volumes/p/project1/assets/env/Forest',
            'cache/Tree.abc'
        ]

        self.assertEqual(output, expected_output)

    def test_remapping_platform_or_path_style_unknown(self):
        map = {'Windows': ['L:\\', 'P:\\'],
               'Linux': ['/mnt/l', '/mnt/p'],
               'Mac': ['/Volumes/l', '/Volumes/p']}
        remaper = Remapper(map)

        input = ['L:\\temp',
                 'P:/project1/textures\grass.tga',
                 'P:\project1\\assets\env\Forest',
                 'cache\Tree.abc',
                 '/mnt/p/project1/assets/prop/Box',
                 '/mnt/p/project1/textures/wood.tga',
                 '/Volumes/l/project2/input/20190117',
                 '/Volumes/l/project2/shots'
                 ]
        output = remaper.remap(input, 'Linux')
        expected_output = [
            '/mnt/l/temp',
            '/mnt/p/project1/textures/grass.tga',
            '/mnt/p/project1/assets/env/Forest',
            'cache/Tree.abc',
            '/mnt/p/project1/assets/prop/Box',
            '/mnt/p/project1/textures/wood.tga',
            '/mnt/l/project2/input/20190117',
            '/mnt/l/project2/shots'
        ]

        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
