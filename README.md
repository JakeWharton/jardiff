# Jardiff

`jardiff` is a Python script which quickly creates diffs of the public API
between two JAR files. This gives you a quick diff without the overhead of a
tool like JDiff. It also supports extracting the `classes.jar` from inside of
Android's AAR format. 

```
$ ./jardiff.py support-v4-19.0.0.jar support-v4-19.1.0.jar
```
```diff
--- support-v4-19.0.0.jar
+++ support-v4-19.1.0.jar
@@ -222,6 +222,7 @@
   public abstract android.support.v4.app.Fragment getFragment(android.os.Bundle, java.lang.String);
   public abstract java.util.List<android.support.v4.app.Fragment> getFragments();
   public abstract android.support.v4.app.Fragment$SavedState saveFragmentInstanceState(android.support.v4.app.Fragment);
+  public abstract boolean isDestroyed();
   public abstract void dump(java.lang.String, java.io.FileDescriptor, java.io.PrintWriter, java.lang.String[]);
   public static void enableDebugLogging(boolean);
 }
@@ -743,24 +744,16 @@
   public static final int SCALE_MODE_FILL;
   public static final int COLOR_MODE_MONOCHROME;
   public static final int COLOR_MODE_COLOR;
+  public static final int ORIENTATION_LANDSCAPE;
+  public static final int ORIENTATION_PORTRAIT;
   public static boolean systemSupportsPrint();
   public android.support.v4.print.PrintHelper(android.content.Context);
   public void setScaleMode(int);
   public int getScaleMode();
   public void setColorMode(int);
   public int getColorMode();
-  public void printBitmap(java.lang.String, android.graphics.Bitmap);
-  public void printBitmap(java.lang.String, android.net.Uri) throws java.io.FileNotFoundException;
-}
-public class android.support.v4.print.PrintHelperKitkat {
-  public static final int SCALE_MODE_FIT;
-  public static final int SCALE_MODE_FILL;
-  public static final int COLOR_MODE_MONOCHROME;
-  public static final int COLOR_MODE_COLOR;
-  public void setScaleMode(int);
-  public int getScaleMode();
-  public void setColorMode(int);
-  public int getColorMode();
+  public void setOrientation(int);
+  public int getOrientation();
   public void printBitmap(java.lang.String, android.graphics.Bitmap);
   public void printBitmap(java.lang.String, android.net.Uri) throws java.io.FileNotFoundException;
 }
@@ -1585,6 +1578,8 @@
   public void setDrawerLockMode(int, android.view.View);
   public int getDrawerLockMode(int);
   public int getDrawerLockMode(android.view.View);
+  public void setDrawerTitle(int, java.lang.CharSequence);
+  public java.lang.CharSequence getDrawerTitle(int);
   public void requestLayout();
   public void computeScroll();
   public boolean onInterceptTouchEvent(android.view.MotionEvent);
@@ -1763,6 +1758,25 @@
   public void draw(android.graphics.Canvas);
   public android.view.ViewGroup$LayoutParams generateLayoutParams(android.util.AttributeSet);
 }
+public interface android.support.v4.widget.SwipeRefreshLayout$OnRefreshListener {
+  public abstract void onRefresh();
+}
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
 public abstract class android.support.v4.widget.ViewDragHelper$Callback {
   public android.support.v4.widget.ViewDragHelper$Callback();
   public void onViewDragStateChanged(int);
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
