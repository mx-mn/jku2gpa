# JKU "Vollständiger Studienerfolg" to ECTS weighted GPA

Just a quick an dirty script to calculate the ECTS-weighted grade from the pdf you get from JKU.

> Note: It might not work for your PDF. The document is not well structured and if there are different table names or something, it probably doesnt work right away.
But, it should be easy to debug and maybe easy to fix.

Maybe it is helpful for anyone.

```
% python -m venv venv 
% source venv/bin/activate
(venv) % pip install PyMuPDF pandas
```

