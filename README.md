# Markdown Image Uploader

Python implement tool for uploading and backuping all images in markdown to AliCloud OSS

## Getting Started

### Configure: 

- configure file path: `$HOME/.oss/oss.conf`

```json
{
	"endpoint": "oss-cn-beijing.aliyuncs.com",
	"ak": "Your AccessKey",
	"sk": "Your SecretKey",
	"bucket": "Your Bucket Name"
}
```

### backup

specify your markdown path and backup target directory simply by:

```shell
$ python markdown.py backup example.md --dst ./backup
```

### upload

Upload all images in the specified markdown file to AliCloud OSS:

```shell
$ python markdown.py backup example.md
```

## Requirements

- Python 3.5 or higher
- requests
- oss2
- pillow

Install python package dependencies by running:

```shell
pip install -r requirements.txt
```

## Authors

* **Prince** - *Initial work* - [Prince's blog](https://blog.prince2015.club)
* Contact with me: [Email](princewang1994@gmail.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## TODO

- [ ] More picture bed, QiNiu, Flickr, Weibo
- [ ] Debugging 