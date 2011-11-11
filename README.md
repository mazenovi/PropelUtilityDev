What is PropelUtility ?
------------
**Propel Utility** is a python extension for MySQLWorkbench to manage your [Propel](http://www.propelorm.org) schemas.

Using **Propel Utility** add following funcitonnalities to your MySQLWorkbench :

* Create and convert to [Propel](http://www.propelorm.org) XML schema format an existing MySQLWorkbench shcema (*.mwb file)
* Manage all the [Propel](http://www.propelorm.org)'s XML schema elements unsupported by MySQLWorkbench

As **Propel Utility** is a python extension, so it can be used on any MySQLWorkbench anabled platform (Mac OS, Linux, Windows)

What PropelUtility is not ...
------------
* **PropelUtility** does not allow edition for data already managed with MySQLWorkbench
* **PropelUtility** can't convert Propel schema to YAML format (use symfony propel:schema-to-yml instead)

PropelUtility
================

Installation
------------

### Get the code

First, place the full project (i.e. `propel_utility_grt.py` and `PropelUtility` folder) in your MySQLWorkbench installation **modules** folder.

It can be in MySQLWorkbench's installation folder, with a path like this:

* `C:\Program Files\mysql-workbench\modules`
* ou `/usr/lib/mysql-workbench/modules` for linux

or even better in your user folder, with a path like this:

* `C:\Users\username\AppData\Roaming\MySQL\Workbench\modules`
* `/home/username/.mysql/workbench/modules` for linux
 

#### via the command line

`git clone git://github.com/mazenovi/PropelUtility.git`

#### From archive

unzip archive downloaded from [PropelUtility's github page](https://github.com/mazenovi/PropelUtility).
  
### Install in MySQLWorkbench

Open your MySQLWorkbench, and go to `"Scripting" -> "Install Plugin / Module ..."`
Browse to the `propel_utility_grt.py` file you just copied, select, and restart MySQLWorkbench.

You're done !

    **N.B.** It's not exactly  the way to install a plugin. As PropelUtility is split in several files, 
    you have to copy all project's files in the "modules" folder by hand, before installation in MySQLWrokbench.

usage
------------

### General information

**PropelUtility** add two new entries to MySQLWorkbench in `"Plugins" -> "Catalog"` :

* `"Propel Utility"`
* `"Propel Erase All Data"`

Any change on the Propel data with Propel Utility  will be validated after a click on the "OK" Button.

If "CANCEL" is clicked, changes will be lost.

To definitely save the Propel data, you should remember to save the .mwb file
    
### Field types

#### non-editable fields

information purpose only. Can be edited through MySQLworkbench but not using **PropelUtility**.

#### editable fields

Clicking on those fields make them editable. Enter the new value to change it.

#### editable fields with choices list

Two ways are available to edit this kind of fields :

* Single clicking on those fields make them editable.
* Double clicking show a list of choices.

You can wether use one of the suggested value by clicking on it and then press the "select this value", 
or enter a custom value.

    N.B. it seems that the choices are unavailable on linux.

tabs
------------

* Database can manage attributes for [`<database />`] (http://www.propelorm.org/reference/schema.html#database_element) xml tag  
* Tables can manage attributes for [`<table />`] (http://www.propelorm.org/reference/schema.html#table_element) xml tag 
* Columns can manage attributes for [`<column />`] (http://www.propelorm.org/reference/schema.html#column_element) xml tag 
* Foreign Keys can manage attributes for [`<foreign-key />`] (http://www.propelorm.org/reference/schema.html#foreignkey_element) xml tag 
* Indices show only attributes for  [`<index />`] (http://www.propelorm.org/reference/schema.html#index_element) et [`<unique/>`] (http://www.propelorm.org/reference/schema.html#unique_element) xml tags
* Behaviors can manage Behaviors for each table ([`<behavior />`] (http://www.propelorm.org/cookbook/writing-behavior.html) xml tag) and all associated parametrs ([`<parameter />`] ((http://www.propelorm.org/cookbook/writing-behavior.html)) xml tag)
* Export can export data managed with previous tab with this rule: required attributes are always exported, and optional attributes will be exported only if associated value is different from defaut value.

customization
------------

You can choose, order, resize evry fields by editing the "fields_list" list in associated tab class (for example PropelTabDatabase.py for Database tab)
 
You can add your own behaviors by adding new items to PropelBehavior.behaviors and PropelBehavior.fields['name']['items'] lists

Propel Erase all data
================

This entry can erase all Propel data managed by PropelUtility and only this data (MySQLWorkbench data will not be affected)

TODO
================
* add an individual export box for each indice (<index /> or <unique />)
* add "single inheritance" support
* add a "Settings" tab to choose which column are showing or not in each tab 
* add an "Import" tab to create MySQLWorkbench schema (*.mwb file) from an existing Propel schema.xml