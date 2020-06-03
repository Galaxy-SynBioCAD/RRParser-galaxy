# Galaxy RetroRules wrapper


## Prerequisites

As RetroRules is a docker galaxy tool, a Docker engine has to be reachable from Galaxy host.

* The Galaxy Project - [Galaxy](https://galaxyproject.org)
* Docker - [Install](https://docs.docker.com/install/)

## Installing

* Create a new section in the Galaxy config file `config/tool_conf.xml` and paste the following:
```
<section id="sbc-rs" name="SynBioCAD RetroRules">
  <tool file="rpTools/RetroRules/wrap.xml" />
</section>
```

* Make sure that the following entry exists under Galaxy's destination tag in `config/tool_conf.xml`:
```
<destination id="docker" runner="local">
  <param id="docker_enabled">true</param>
  <param id="docker_sudo">false</param>
  <param id="docker_set_user">root</param>
  <param id="docker_auto_rm">true</param>
</destination>
```

And that the destination of the tool is referred under the tools tag in `config/job_conf.xml`:

```
<tool id="RetroRules" destination="docker" />
```


## Built With

* [Galaxy](https://galaxyproject.org) - The Galaxy project


## Authors

* Melchior du Lac
* Joan Hérisson
* Thomas Duigou

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
