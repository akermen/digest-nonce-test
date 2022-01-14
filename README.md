## digest-nonce-test

Simple test setup to demonstrate digest authentication `nonce` value uniqueness of the [Libmicrohttpd](https://www.gnu.org/software/libmicrohttpd/) library. Check the **libmicrohttpd** mailing list [thread](https://lists.gnu.org/archive/html/libmicrohttpd/2022-01/msg00000.html) for details.


### Build and start server

```
make
```


### Run tests

```
make test
```

```
make test-second
```
