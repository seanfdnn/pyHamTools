# Reverse Beacon Network client for Python

This is both a library and cli tool, under the package `rbn`

## Installation

pyRBN can be installed from PYPI:

```sh
python3 -m pip install rbn
```

and imported as:

```python
import rbn
```

## CLI Usage

```text
usage: rbn [-h] -c CALLSIGN [-b {630m,160m,80m,60m,40m,30m,20m,17m,15m,12m,10m,6m,4m,2m}] [-m {cw,rtty,psk31,psk63,ft8,ft4}] [-f FILTER_CALL]

CLI frontend to the Reverse Beacon Network

optional arguments:
  -h, --help            show this help message and exit
  -c CALLSIGN, --callsign CALLSIGN
                        Your callsign
  -b {630m,160m,80m,60m,40m,30m,20m,17m,15m,12m,10m,6m,4m,2m}, --band {630m,160m,80m,60m,40m,30m,20m,17m,15m,12m,10m,6m,4m,2m}
                        Band to filter by (this can be passed multiple times)
  -m {cw,rtty,psk31,psk63,ft8,ft4}, --mode {cw,rtty,psk31,psk63,ft8,ft4}
                        Mode to filter by (this can be passed multiple times)
  -f FILTER_CALL, --filter-call FILTER_CALL
                        Callign to filter by (this can be passed multiple times)
```

## Example library usage

The [`__main__.py`](https://github.com/Ewpratten/pyRBN/blob/master/rbn/__main__.py) file is kept fairly simple as an example of using this library.
