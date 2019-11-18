URLExploder – simple plugin, explodes URL into multiline block of base-part and sorted-decoded query string params or collapses exploded URL back into flat form.

# Usage
## Explode
```
https://example.com/slug/?one=1&two=2&three=3&three=4?four=4&five=%D1%82%D0%B5%D1%81%D1%82#fragment
```
→
```
https://example.com/slug/
?one=1
&three=3
&three=4
&two=2
?five=тест
&four=4
#fragment
```

## Implode
```
https://example.com/slug/
?one=1
&three=3
&three=4
&two=2
?five=тест
&four=4
#fragment
```
→
```
https://example.com/slug/?one=1&three=3&three=4&two=2?five=%D1%82%D0%B5%D1%81%D1%82&four=4#fragment
```

## Explode (as-is)
```
https://example.com/slug/?one=1&two=2&three=3&three=4?four=4&five=%D1%82%D0%B5%D1%81%D1%82#fragment
```
→
```
https://example.com/slug/
?one=1
&two=2
&three=3
&three=4
?four=4
&five=%D1%82%D0%B5%D1%81%D1%82
#fragment
```

## Implode (as-is)
```
https://example.com/slug/
?one=1
&two=2
&three=3
&three=4
?four=4
&five=%D1%82%D0%B5%D1%81%D1%82
#fragment
```
→
```
https://example.com/slug/?one=1&two=2&three=3&three=4?four=4&five=%D1%82%D0%B5%D1%81%D1%82#fragment
```

# Installation
Supports Sublime Text 2 and 3.
Use your version number in directory path.

## OS X
```
cd ~/"Library/Application Support/Sublime Text 2/Packages"
git clone https://github.com/gzzz/sublime-url-exploder.git URLExploder
```

## Windows
```
cd %AppData%\Sublime Text 2\Packages\
git clone https://github.com/gzzz/sublime-url-exploder.git URLExploder
```
