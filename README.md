# Dunbo - Bandwidth Analysis Tool

Dunbo is a python tool for bandwidth analysis including support for TCP & UDP connections.

## Installation

Please notice that Dunbo has been developed under plotly library
which you find under https://plot.ly/. In order to run Dunbo successfuly, you will first need to download plotly to your local machine.

In order to do so, please run the following command:
`pip install plotly`

If you face any issues or have troubleshooting, please visit the following URL:

https://plot.ly/python/getting-started/

## Usage

In order to use Dunbo you will need to run execute.py script with a command line arguments.

Arguments list:

`host - host address of the current script runner (ip address)`

`port - which port does the current script listens to`

`type - 2 options: 's' - stands for server or 'c' which stands for client`

`debug = True / False - please desable debug under production environment`

`visualization - True / False - stands for graph visualization for the bandwidth summary`

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License

The content of this project itself is licensed under the Creative Commons Attribution 3.0 license, and the underlying source code used
to format and display that content is licensed under the MIT license.
