using System;
using Autodesk.Revit.UI;
using Autodesk.Revit.DB;

using PyRevitLabs.PyRevit.Runtime;

namespace HelloWorld
{
   public class MyCSharpCommand : IExternalCommand
   {
      // define the execparams field
      public ExecParams execParams;

      public Result Execute(ExternalCommandData revit, ref string message, ElementSet elements)
      {
         Console.WriteLine(execParams.ScriptPath); 
         return Result.Succeeded;
      }
   }
}