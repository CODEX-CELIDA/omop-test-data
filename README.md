# CELIDA OMOP Test Data Generator

The tdg creates OMOP-CDM conforming, clinically plausible test data in order to test the CELIDA [execution engine][EE] and
therefore also the [user interface][UI].

## Usage

The tdg is a command line tool. It can be used as follows:

```
python random_data_generator.py [n]
```

where `n` is the number of patients to be generated. If `n` is not specified, the default value of 10 is used.

## Configuration

Copy the `.credentials.sample.json` file to .credentials.json and fill in the credentials for the OMOP CDM database connection.


## Contributing

We welcome contributions to this repository! If you have any suggestions or bug reports, please open an issue or a pull request.

## Contact

For more information about the CODEX-CELIDA project, please visit <https://github.com/CODEX-CELIDA>.

[EE]: https://github.com/CODEX-CELIDA/execution-engine
[UI]: https://github.com/CODEX-CELIDA/user-interface
