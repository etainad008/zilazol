# How to Request Data from File Servers

In this document, we list ways to request and download resources from different file servers.

- [How to Request Data from File Servers](#how-to-request-data-from-file-servers)
  - [Background](#background)
  - [Server Types](#server-types)
    - [Cerberus](#cerberus)
      - [Authentication and File Access](#authentication-and-file-access)
    - [Shufersal (7290027600007)](#shufersal-7290027600007)
      - [Authentication and File Access](#authentication-and-file-access-1)

## Background

Most chains use a centerlized Cerberus FTP server, with a user for each chain. Others have specialized sites.

## Server Types

### Cerberus

Hosted at `https://url.publishedprices.co.il/`, this centralized server includes the following chains and their prices:

| Chain Name (username) | Password | Chain ID      |
| :-------------------- | :------- | :------------ |
| doralon               |          | 7290492000005 |
| TivTaam               |          | 7290873255550 |
| HaziHinam             |          | 7290700100008 |
| yohananof             |          | 7290100700006 |
| osherad               |          | 7290103152017 |
| SalachD               | 12345    | 7290526500006 |
| Stop_Market           |          | 7290639000004 |
| politzer              |          | 7291059100008 |
| Paz_bo                | paz468   | 7290644700005 |
| freshmarket           |          | 7290876100000 |
| Keshet                |          | 7290785400000 |
| RamiLevi              |          | 7290058140886 |
| SuperCofixApp         |          | 7291056200008 |

This server is `CerberusFTPServer/12.0` (version might change in the future).

#### Authentication and File Access

1. Perform a `GET` requets to `/login`. The server will return a cookie named `cftpSID` (probably "Cerberus FTP Sesstion ID"), as well as a `csrftoken` saved in a `<meta>` tag.

2. Sign in with your selected user. This is done by making a `POST` request to `/login/user`. You can add a `r` parameter for redirection. Additionally, a `Submit=Sign+in` parameter must be passed in order to sign in. Here is an example:

   ```HTTP
       r=&username=SalachD&password=12345&Submit=Sign+in&csrftoken=<csrftoken-here>
   ```

   If you authenticated properly, the server should respond with a `302` status redirect to `/file`, with a new `cftpSID` cookie.

3. Using the new cookie, make a `GET` request for `/file`. From a `<meta>` tag in response, extract the new `csrftoken` which will be needed to query the serve's file list.

4. To get a list of files, you can make another `POST` request to `/file/json/dir` with some parameters. There is control for every "data column" (e.g. date, size, name) regarding sorting and search. We are mainly interested in controlling how many files we want, and getting the type of file we want (PricesFull, Stores, etc.).

   For exmaple, we can use the parameter `iDisplayLength` to control the amount of files to be queried from the server, or `sSearch` to search the names of the files.

   The `csrftoken` we got from `/file` needs to be passed in as a parameter as well.

5. The response content is a JSON object, and access to the list itself is via the `aaData` key. Here, we can sort the list as we like, using the `time` field, for example.

6. We can now make a `GET` request to `/file/d/<file-name>` to get a compressed file (a .gz is used).

### Shufersal (7290027600007)

The Shufersal file server is hosted at `https://prices.shufersal.co.il/`. This is a `Microsoft-IIS/10.0` server.

#### Authentication and File Access

Fortunately, this server does not require any user sign in, which simplfies the query process.

1. Perform a `GET` request to root `/`. The response includes the page's HTML, but more importantly two cookies `ARRAffinity` and `ARRAffinitySameSite` with tokens. For the time being, they look identical.

2. Make another `GET` request to `/FileObject/UpdateCategory` to change the file list. Here, we can use query parameters such as `catID` to choose our file category or `storeId` to choose which store we wan to query from (more parameters like `sort` are not covered here, but you can see them being sent if you filter/sort through th UI).

3. Parse the response's HTML to get the file you want. The file list is in a table, and parsing the rows is very easy. When you have found a file(s) you want to download, you can use the download link provided on each entry via the `<a>` tag.

4. Profit.
