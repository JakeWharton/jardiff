# Jar Diff

`jardiff` is a Python script which quickly creates diffs of the public API
between two JAR files. This gives you a quick diff without the overhead of a
tool like JDiff. It also supports extracting the `classes.jar` from inside of
Android's AAR format. 

```
$ ./jardiff.py support-v4-19.0.0.jar support-v4-19.1.0.jar
```
```diff
diff -U 0 -N support-v4-19.0.0/android.support.v4.app.FragmentManager support-v4-19.1.0/android.support.v4.app.FragmentManager
--- support-v4-19.0.0/android.support.v4.app.FragmentManager	2014-06-26 19:59:59.000000000 -0700
+++ support-v4-19.1.0/android.support.v4.app.FragmentManager	2014-06-26 19:59:59.000000000 -0700
@@ -22,0 +23 @@
+  public abstract boolean isDestroyed();
diff -U 0 -N support-v4-19.0.0/android.support.v4.print.PrintHelper support-v4-19.1.0/android.support.v4.print.PrintHelper
--- support-v4-19.0.0/android.support.v4.print.PrintHelper	2014-06-26 19:59:59.000000000 -0700
+++ support-v4-19.1.0/android.support.v4.print.PrintHelper	2014-06-26 19:59:59.000000000 -0700
@@ -5,0 +6,2 @@
+  public static final int ORIENTATION_LANDSCAPE;
+  public static final int ORIENTATION_PORTRAIT;
@@ -11,0 +14,2 @@
+  public void setOrientation(int);
+  public int getOrientation();
diff -U 0 -N support-v4-19.0.0/android.support.v4.print.PrintHelperKitkat support-v4-19.1.0/android.support.v4.print.PrintHelperKitkat
--- support-v4-19.0.0/android.support.v4.print.PrintHelperKitkat	2014-06-26 19:59:59.000000000 -0700
+++ support-v4-19.1.0/android.support.v4.print.PrintHelperKitkat	1969-12-31 16:00:00.000000000 -0800
@@ -1,12 +0,0 @@
-public class android.support.v4.print.PrintHelperKitkat {
-  public static final int SCALE_MODE_FIT;
-  public static final int SCALE_MODE_FILL;
-  public static final int COLOR_MODE_MONOCHROME;
-  public static final int COLOR_MODE_COLOR;
-  public void setScaleMode(int);
-  public int getScaleMode();
-  public void setColorMode(int);
-  public int getColorMode();
-  public void printBitmap(java.lang.String, android.graphics.Bitmap);
-  public void printBitmap(java.lang.String, android.net.Uri) throws java.io.FileNotFoundException;
-}
diff -U 0 -N support-v4-19.0.0/android.support.v4.widget.DrawerLayout support-v4-19.1.0/android.support.v4.widget.DrawerLayout
--- support-v4-19.0.0/android.support.v4.widget.DrawerLayout	2014-06-26 19:59:59.000000000 -0700
+++ support-v4-19.1.0/android.support.v4.widget.DrawerLayout	2014-06-26 19:59:59.000000000 -0700
@@ -19,0 +20,2 @@
+  public void setDrawerTitle(int, java.lang.CharSequence);
+  public java.lang.CharSequence getDrawerTitle(int);
diff -U 0 -N support-v4-19.0.0/android.support.v4.widget.SwipeRefreshLayout support-v4-19.1.0/android.support.v4.widget.SwipeRefreshLayout
--- support-v4-19.0.0/android.support.v4.widget.SwipeRefreshLayout	1969-12-31 16:00:00.000000000 -0800
+++ support-v4-19.1.0/android.support.v4.widget.SwipeRefreshLayout	2014-06-26 19:59:59.000000000 -0700
@@ -0,0 +1,16 @@
+public class android.support.v4.widget.SwipeRefreshLayout extends android.view.ViewGroup {
+  public android.support.v4.widget.SwipeRefreshLayout(android.content.Context);
+  public android.support.v4.widget.SwipeRefreshLayout(android.content.Context, android.util.AttributeSet);
+  public void onAttachedToWindow();
+  public void onDetachedFromWindow();
+  public void setOnRefreshListener(android.support.v4.widget.SwipeRefreshLayout$OnRefreshListener);
+  public void setRefreshing(boolean);
+  public void setColorScheme(int, int, int, int);
+  public boolean isRefreshing();
+  public void draw(android.graphics.Canvas);
+  public void onMeasure(int, int);
+  public boolean canChildScrollUp();
+  public boolean onInterceptTouchEvent(android.view.MotionEvent);
+  public void requestDisallowInterceptTouchEvent(boolean);
+  public boolean onTouchEvent(android.view.MotionEvent);
+}
diff -U 0 -N support-v4-19.0.0/android.support.v4.widget.SwipeRefreshLayout$OnRefreshListener support-v4-19.1.0/android.support.v4.widget.SwipeRefreshLayout$OnRefreshListener
--- support-v4-19.0.0/android.support.v4.widget.SwipeRefreshLayout$OnRefreshListener	1969-12-31 16:00:00.000000000 -0800
+++ support-v4-19.1.0/android.support.v4.widget.SwipeRefreshLayout$OnRefreshListener	2014-06-26 19:59:59.000000000 -0700
@@ -0,0 +1,3 @@
+public interface android.support.v4.widget.SwipeRefreshLayout$OnRefreshListener {
+  public abstract void onRefresh();
+}
```


License
-------

    Copyright 2014 Jake Wharton

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
